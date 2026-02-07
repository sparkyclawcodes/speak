---
name: speak
description: Generate speech audio from text using Qwen3-TTS on a local NVIDIA GPU. Use when the user wants to convert text to speech, create voice audio, generate .wav files from text, or use TTS. Supports voice selection and style instructions (e.g. "whisper", "Very happy."). Requires Docker with GPU support and an NVIDIA GPU. Uses a persistent background server so requests after the first take ~2s.
---

# speak

Generate speech from text via the `speak` CLI, which runs Qwen3-TTS (CustomVoice, 1.7B) in a persistent Docker server with GPU acceleration.

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
| `--stop` | Stop the background TTS server |
| `--help, -h` | Show help |

First call starts a background server (~30s to load model). Subsequent calls take ~2s.

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
speak --stop
```

## Notes

- Output is 24kHz mono PCM WAV
- Generation takes ~2s per short sentence once server is warm
- All status output goes to stderr; stdout stays clean
- Server persists across calls until `speak --stop` or reboot
