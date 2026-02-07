#!/usr/bin/env python3
"""Generate speech from text using Qwen3-TTS CustomVoice model."""

import argparse
import os
import sys
import time
import warnings

# Silence noisy warnings before any imports trigger them
warnings.filterwarnings("ignore")
os.environ["PYTHONWARNINGS"] = "ignore"

import logging

logging.disable(logging.WARNING)

from pathlib import Path

import soundfile as sf
import torch
from qwen_tts import Qwen3TTSModel

MODEL_HUB_ID = "Qwen/Qwen3-TTS-12Hz-1.7B-CustomVoice"
MODEL_CACHE = Path.home() / ".cache/huggingface/hub" / ("models--" + MODEL_HUB_ID.replace("/", "--"))


def resolve_model_path():
    """Use local snapshot if available, otherwise fall back to hub ID."""
    snapshots = MODEL_CACHE / "snapshots"
    if snapshots.is_dir():
        revs = sorted(snapshots.iterdir())
        if revs:
            return str(revs[-1])
    return MODEL_HUB_ID


def main():
    parser = argparse.ArgumentParser(description="Generate speech from text")
    parser.add_argument("--text", required=True, help="Text to speak")
    parser.add_argument("--voice", default="Vivian", help="Speaker voice")
    parser.add_argument("--output", required=True, help="Output .wav path")
    parser.add_argument("--language", default="English", help="Language")
    parser.add_argument("--instruct", default="", help="Voice style instruction")
    args = parser.parse_args()

    model_path = resolve_model_path()
    print(f"Loading model...", file=sys.stderr)
    t0 = time.time()
    model = Qwen3TTSModel.from_pretrained(
        model_path,
        device_map="cuda:0",
        dtype=torch.bfloat16,
    )
    t_load = time.time() - t0
    print(f"Model loaded in {t_load:.1f}s", file=sys.stderr)

    instruct_msg = f", instruct={args.instruct!r}" if args.instruct else ""
    print(f"Generating speech (voice={args.voice}{instruct_msg})...", file=sys.stderr)
    t0 = time.time()

    kwargs = dict(
        text=args.text,
        speaker=args.voice,
        language=args.language,
    )
    if args.instruct:
        kwargs["instruct"] = args.instruct

    wavs, sample_rate = model.generate_custom_voice(**kwargs)
    t_gen = time.time() - t0

    wav = wavs[0]
    duration = len(wav) / sample_rate
    rtf = t_gen / duration if duration > 0 else float("inf")
    print(
        f"Generated {duration:.2f}s of audio in {t_gen:.2f}s (RTF={rtf:.2f})",
        file=sys.stderr,
    )

    sf.write(args.output, wav, sample_rate)
    print(f"Saved to {args.output}", file=sys.stderr)


if __name__ == "__main__":
    main()
