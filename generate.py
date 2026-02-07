#!/usr/bin/env python3
"""Generate speech from text using Qwen3-TTS CustomVoice model."""

import argparse
import sys
import time

import soundfile as sf
import torch
from qwen_tts import Qwen3TTSModel


def main():
    parser = argparse.ArgumentParser(description="Generate speech from text")
    parser.add_argument("--text", required=True, help="Text to speak")
    parser.add_argument("--voice", default="Vivian", help="Speaker voice")
    parser.add_argument("--output", required=True, help="Output .wav path")
    parser.add_argument("--language", default="English", help="Language")
    args = parser.parse_args()

    print("Loading model...", file=sys.stderr)
    t0 = time.time()
    model = Qwen3TTSModel.from_pretrained(
        "Qwen/Qwen3-TTS-12Hz-1.7B-CustomVoice",
        device_map="cuda:0",
        dtype=torch.bfloat16,
    )
    t_load = time.time() - t0
    print(f"Model loaded in {t_load:.1f}s", file=sys.stderr)

    print(f"Generating speech (voice={args.voice})...", file=sys.stderr)
    t0 = time.time()
    wavs, sample_rate = model.generate_custom_voice(
        text=args.text,
        speaker=args.voice,
        language=args.language,
    )
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
