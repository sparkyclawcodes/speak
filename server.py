#!/usr/bin/env python3
"""Persistent TTS server — loads model once, serves requests over HTTP."""

import io
import os
import sys
import time
import warnings

warnings.filterwarnings("ignore")
os.environ["PYTHONWARNINGS"] = "ignore"

import logging

logging.disable(logging.WARNING)

from pathlib import Path

import soundfile as sf
import torch
from fastapi import FastAPI
from fastapi.responses import Response
from pydantic import BaseModel
from qwen_tts import Qwen3TTSModel

MODEL_HUB_ID = "Qwen/Qwen3-TTS-12Hz-1.7B-CustomVoice"
MODEL_CACHE = Path.home() / ".cache/huggingface/hub" / ("models--" + MODEL_HUB_ID.replace("/", "--"))


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


class GenerateRequest(BaseModel):
    text: str
    voice: str = "Vivian"
    language: str = "English"
    instruct: str = ""


@app.post("/generate")
def generate(req: GenerateRequest):
    t0 = time.time()
    kwargs = dict(text=req.text, speaker=req.voice, language=req.language)
    if req.instruct:
        kwargs["instruct"] = req.instruct
    wavs, sample_rate = model.generate_custom_voice(**kwargs)
    t_gen = time.time() - t0

    wav = wavs[0]
    duration = len(wav) / sample_rate
    rtf = t_gen / duration if duration > 0 else float("inf")
    print(f"Generated {duration:.2f}s audio in {t_gen:.2f}s (RTF={rtf:.2f}) voice={req.voice}", file=sys.stderr)

    buf = io.BytesIO()
    sf.write(buf, wav, sample_rate, format="WAV")
    return Response(content=buf.getvalue(), media_type="audio/wav")


@app.get("/health")
def health():
    return {"status": "ok"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=9800)
