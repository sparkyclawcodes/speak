---
name: speak
description: Generate speech audio from text using Qwen3-TTS on a local NVIDIA GPU. Use when the user wants to convert text to speech, create voice audio, generate .wav files from text, or use TTS. Requires Docker with GPU support and an NVIDIA GPU.
---

# speak

Generate speech from text via the `speak` CLI, which runs Qwen3-TTS (CustomVoice, 1.7B) inside a Docker container with GPU acceleration.

## Prerequisites

- `speak` must be on PATH (typically symlinked to `~/.local/bin/speak`)
- Docker with `--gpus all` support
- NVIDIA GPU
- First run builds the Docker image (~2-3 min) and downloads the model (~4GB to `~/.cache/huggingface`)

## Usage

```bash
speak [OPTIONS] TEXT
```

| Option | Description |
|---|---|
| `--voice, -v` | Speaker voice (default: Vivian) |
| `--output, -o` | Output .wav path (default: output.wav) |
| `--help, -h` | Show help |

## Voices

`aiden` `dylan` `eric` `ono_anna` `ryan` `serena` `sohee` `uncle_fu` `vivian`

## Examples

```bash
# Basic usage
speak "Hello world" -o hello.wav

# Specific voice
speak -v ryan -o greeting.wav "Good morning everyone"

# Different language speaker
speak -v sohee -o korean.wav "안녕하세요"
```

## Notes

- Output is 24kHz mono PCM WAV
- Generation takes ~2-3s per short sentence (RTF ~1.5x on DGX Spark)
- Model loading adds ~30-40s on first invocation per container run
- All status/timing output goes to stderr; stdout stays clean
- The container is ephemeral (`--rm`), model weights are cached on the host
