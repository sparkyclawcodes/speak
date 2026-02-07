---
name: speak
description: Generate speech audio from text using Qwen3-TTS on a local NVIDIA GPU. Use when the user wants to convert text to speech, create voice audio, generate .wav files from text, or use TTS. Supports voice selection, style instructions, and WebSocket streaming for real-time audio output. Requires Docker with GPU support and an NVIDIA GPU.
---

# speak

Generate speech from text via the `speak` CLI or streaming API. Runs Qwen3-TTS (CustomVoice, 1.7B) in a persistent Docker server with GPU acceleration.

## CLI

```bash
speak [OPTIONS] -o OUTPUT TEXT
```

| Option | Description |
|---|---|
| `--voice, -v` | Speaker voice (default: Vivian) |
| `--output, -o` | Output .wav path (required) |
| `--instruct, -i` | Voice style instruction, e.g. "whisper" or "Very happy." (optional) |
| `--stop` | Stop the background TTS server |

Voices: `vivian` `serena` `uncle_fu` `dylan` `eric` `ryan` `aiden` `ono_anna` `sohee`

## Streaming API

WebSocket at `ws://localhost:9800/ws/stream` for streaming audio output.

```
Send: JSON {"text": "...", "voice": "...", "instruct": "..."}
Recv: binary int16 PCM (24kHz mono) chunks
Recv: JSON {"done": true, "duration": float, "sample_rate": 24000}
```

## REST API

```
POST http://localhost:9800/generate
Body: {"text": "...", "voice": "...", "instruct": "..."}
Returns: audio/wav
```

## Examples

```bash
speak -o hello.wav "Hello world"
speak -v ryan -i "Very happy." -o excited.wav "I got promoted!"
```
