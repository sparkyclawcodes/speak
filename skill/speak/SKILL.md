---
name: speak
description: Generate speech audio from text using Qwen3-TTS on a local NVIDIA GPU. Use when the user wants to convert text to speech, create voice audio, generate .wav files from text, or use TTS. Supports voice selection and style instructions (e.g. "whisper", "Very happy."). Requires Docker with GPU support and an NVIDIA GPU.
---

# speak

Generate speech from text via the `speak` CLI, which runs Qwen3-TTS (CustomVoice, 1.7B) inside a Docker container with GPU acceleration.

## Prerequisites

- `speak` must be on PATH (typically symlinked to `~/.local/bin/speak`)
- Docker with `--gpus all` support
- NVIDIA GPU
- First run builds the Docker image (~5 min, one-time, model weights baked in)

## Usage

```bash
speak [OPTIONS] -o OUTPUT TEXT
```

| Option | Description |
|---|---|
| `--voice, -v` | Speaker voice (default: Vivian) |
| `--output, -o` | Output .wav path (required) |
| `--instruct, -i` | Voice style instruction, e.g. "whisper" or "Very happy." (optional) |
| `--help, -h` | Show help |

## Voices

| Speaker | Description | Native Language |
|---|---|---|
| `vivian` | Bright, slightly edgy young female | Chinese |
| `serena` | Warm, gentle young female | Chinese |
| `uncle_fu` | Seasoned male, low mellow timbre | Chinese |
| `dylan` | Youthful Beijing male | Chinese |
| `eric` | Lively Chengdu male | Chinese |
| `ryan` | Dynamic male, strong rhythmic drive | English |
| `aiden` | Sunny American male | English |
| `ono_anna` | Playful Japanese female | Japanese |
| `sohee` | Warm Korean female | Korean |

## Examples

```bash
speak -o hello.wav "Hello world"
speak -v ryan -o greeting.wav "Good morning everyone"
speak -i "whisper" -o secret.wav "This is a secret"
speak -i "Very happy." -o excited.wav "I just got promoted!"
```

## Notes

- Output is 24kHz mono PCM WAV
- Generation takes ~2-3s per short sentence (RTF ~1.3x on DGX Spark)
- Model loading adds ~35s per container run
- All status/timing output goes to stderr; stdout stays clean
