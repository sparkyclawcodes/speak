# speak

A CLI tool for text-to-speech using [Qwen3-TTS](https://huggingface.co/Qwen/Qwen3-TTS-12Hz-1.7B-CustomVoice) on NVIDIA GPUs.

Wraps the Qwen3-TTS CustomVoice model in a Docker container with a persistent server, so the model loads once and subsequent requests take ~2s.

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

## Usage

```
speak [OPTIONS] -o OUTPUT TEXT

Options:
  --voice, -v      Speaker voice (default: Vivian)
  --output, -o     Output .wav path (required)
  --instruct, -i   Voice style instruction, e.g. "whisper" or "Very happy." (optional)
  --help, -h       Show this help

Server management:
  --stop           Stop the background TTS server
```

On first invocation, `speak` starts a background Docker container that loads the model (~30s). Subsequent calls hit the warm server and return in ~2s. The server persists across calls until you run `speak --stop` or reboot.

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

### Examples

```bash
speak -o hello.wav "Hello world"
speak -v ryan -o greeting.wav "Good morning everyone"
speak -i "whisper" -o secret.wav "This is a secret"
speak -i "Very happy." -o excited.wav "I just got promoted!"
speak -v sohee -o korean.wav "안녕하세요"
speak --stop  # stop the background server
```

## How it works

1. On first run, builds a Docker image (`speak:latest`) with all dependencies and model weights baked in
2. First `speak` call starts a persistent server container (`speak-server`) that loads the model once
3. Requests are sent to the server over HTTP, which generates audio and returns wav bytes
4. Server stays running for instant subsequent calls (~2s per request)

## License

MIT
