#!/usr/bin/env python3
"""Persistent TTS server — loads model once, serves requests over HTTP and WebSocket."""

import io
import json
import os
import sys
import time
import warnings

warnings.filterwarnings("ignore")
os.environ["PYTHONWARNINGS"] = "ignore"

import logging

logging.disable(logging.WARNING)

from pathlib import Path

import numpy as np
import soundfile as sf
import torch
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import Response
from pydantic import BaseModel
from qwen_tts import Qwen3TTSModel

MODEL_HUB_ID = "Qwen/Qwen3-TTS-12Hz-1.7B-CustomVoice"
MODEL_CACHE = Path.home() / ".cache/huggingface/hub" / ("models--" + MODEL_HUB_ID.replace("/", "--"))
SAMPLE_RATE = 24000
CHUNK_SAMPLES = SAMPLE_RATE  # 1 second chunks for streaming


def resolve_model_path():
    snapshots = MODEL_CACHE / "snapshots"
    if snapshots.is_dir():
        revs = sorted(snapshots.iterdir())
        if revs:
            return str(revs[-1])
    return MODEL_HUB_ID


app = FastAPI()
model = None


@app.on_event("startup")
def load_model():
    global model
    model_path = resolve_model_path()
    print(f"Loading model from {model_path}...", file=sys.stderr)
    t0 = time.time()
    model = Qwen3TTSModel.from_pretrained(
        model_path,
        device_map="cuda:0",
        dtype=torch.bfloat16,
    )
    print(f"Model loaded in {time.time() - t0:.1f}s", file=sys.stderr)


def generate_audio(text, voice="Vivian", language="English", instruct=""):
    kwargs = dict(text=text, speaker=voice, language=language)
    if instruct:
        kwargs["instruct"] = instruct
    wavs, sample_rate = model.generate_custom_voice(**kwargs)
    return wavs[0], sample_rate


class GenerateRequest(BaseModel):
    text: str
    voice: str = "Vivian"
    language: str = "English"
    instruct: str = ""


@app.post("/generate")
def generate(req: GenerateRequest):
    """Generate speech, return complete WAV file."""
    t0 = time.time()
    wav, sample_rate = generate_audio(req.text, req.voice, req.language, req.instruct)
    t_gen = time.time() - t0

    duration = len(wav) / sample_rate
    rtf = t_gen / duration if duration > 0 else float("inf")
    print(f"Generated {duration:.2f}s audio in {t_gen:.2f}s (RTF={rtf:.2f}) voice={req.voice}", file=sys.stderr)

    buf = io.BytesIO()
    sf.write(buf, wav, sample_rate, format="WAV")
    return Response(content=buf.getvalue(), media_type="audio/wav")


@app.websocket("/ws/stream")
async def stream_generate(ws: WebSocket):
    """Stream audio generation — send text, receive audio chunks.

    Protocol:
      Client sends: JSON {"text": "...", "voice": "...", "instruct": "...", "language": "..."}
      Server sends: binary (int16 PCM, 24kHz mono) in chunks
      Server sends: JSON {"done": true, "duration": float, "sample_rate": int} when complete
    """
    await ws.accept()

    try:
        while True:
            msg = await ws.receive_text()
            req = json.loads(msg)

            text = req.get("text", "")
            if not text:
                await ws.send_json({"error": "missing text"})
                continue

            voice = req.get("voice", "Vivian")
            language = req.get("language", "English")
            instruct = req.get("instruct", "")

            t0 = time.time()
            wav, sample_rate = generate_audio(text, voice, language, instruct)
            t_gen = time.time() - t0

            duration = len(wav) / sample_rate
            print(f"Stream: {duration:.2f}s audio in {t_gen:.2f}s voice={voice}", file=sys.stderr)

            # Stream audio in chunks as int16 PCM
            pcm = (wav * 32768).astype(np.int16)
            for i in range(0, len(pcm), CHUNK_SAMPLES):
                chunk = pcm[i : i + CHUNK_SAMPLES]
                await ws.send_bytes(chunk.tobytes())

            await ws.send_json({
                "done": True,
                "duration": round(duration, 2),
                "sample_rate": sample_rate,
            })
    except WebSocketDisconnect:
        pass


@app.get("/health")
def health():
    return {"status": "ok"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=9800)
