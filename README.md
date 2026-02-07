# speak

A CLI tool and API for text-to-speech using [Qwen3-TTS](https://huggingface.co/Qwen/Qwen3-TTS-12Hz-1.7B-CustomVoice) on NVIDIA GPUs.

Wraps the Qwen3-TTS CustomVoice model in a Docker container with a persistent server. The model loads once and subsequent requests take ~2s.

## Requirements

- NVIDIA GPU with Docker GPU support (`--gpus all`)
- Docker

Tested on NVIDIA DGX Spark (GB10, CUDA 12.1).

## Install

```bash
git clone https://github.com/sparkyclawcodes/speak.git
ln -s "$(pwd)/speak/speak" ~/.local/bin/speak
```

The Docker image builds automatically on first run (~5 min, one-time). Model weights are baked into the image.

## CLI Usage

```
speak [OPTIONS] -o OUTPUT TEXT

Options:
  --voice, -v      Speaker voice (default: Vivian)
  --output, -o     Output .wav path (required)
  --instruct, -i   Voice style instruction, e.g. "whisper" or "Very happy." (optional)
  --help, -h       Show this help
  --stop           Stop the background TTS server
```

### Examples

```bash
speak -o hello.wav "Hello world"
speak -v ryan -o greeting.wav "Good morning everyone"
speak -i "whisper" -o secret.wav "This is a secret"
speak --stop
```

## Streaming API

WebSocket endpoint for streaming audio output, suitable for phone call APIs and real-time applications.

```
ws://localhost:9800/ws/stream
```

**Protocol:**
```
Client sends: JSON {"text": "...", "voice": "...", "instruct": "...", "language": "..."}
Server sends: binary (int16 PCM, 24kHz mono) in 1-second chunks
Server sends: JSON {"done": true, "duration": float, "sample_rate": 24000}
```

**Example (Python):**
```python
import asyncio, json, websockets

async def stream_tts():
    async with websockets.connect("ws://localhost:9800/ws/stream") as ws:
        await ws.send(json.dumps({"text": "Hello world", "voice": "Vivian"}))
        while True:
            msg = await ws.recv()
            if isinstance(msg, bytes):
                # int16 PCM audio chunk — play or forward
                process_audio(msg)
            else:
                data = json.loads(msg)
                if data.get("done"):
                    break

asyncio.run(stream_tts())
```

### REST API

```
POST http://localhost:9800/generate
Content-Type: application/json
{"text": "...", "voice": "...", "instruct": "...", "language": "..."}
→ audio/wav
```

### Available voices

| Speaker | Description | Native Language |
|---------|-------------|-----------------|
| `vivian` | Bright, slightly edgy young female | Chinese |
| `serena` | Warm, gentle young female | Chinese |
| `uncle_fu` | Seasoned male, low mellow timbre | Chinese |
| `dylan` | Youthful Beijing male, clear natural timbre | Chinese |
| `eric` | Lively Chengdu male, slightly husky brightness | Chinese |
| `ryan` | Dynamic male with strong rhythmic drive | English |
| `aiden` | Sunny American male, clear midrange | English |
| `ono_anna` | Playful Japanese female, light nimble timbre | Japanese |
| `sohee` | Warm Korean female with rich emotion | Korean |

## Companion tool

See [listen](https://github.com/sparkyclawcodes/listen) for speech-to-text using NVIDIA Parakeet-TDT.

## License

MIT
