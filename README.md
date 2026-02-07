# speak

A CLI tool for text-to-speech using [Qwen3-TTS](https://huggingface.co/Qwen/Qwen3-TTS-12Hz-1.7B-CustomVoice) on NVIDIA GPUs.

Wraps the Qwen3-TTS CustomVoice model in a Docker container so you can generate speech from your host machine with a single command.

## Requirements

- NVIDIA GPU with Docker GPU support (`--gpus all`)
- Docker
- ~4GB disk for the model (downloaded on first run, cached in `~/.cache/huggingface`)

Tested on NVIDIA DGX Spark (GB10, CUDA 12.1).

## Install

```bash
git clone https://github.com/sparkyclawcodes/speak.git
ln -s "$(pwd)/speak/speak" ~/.local/bin/speak
```

The Docker image builds automatically on first run (~2-3 min, one-time).

## Usage

```
speak [OPTIONS] TEXT

Options:
  --voice, -v   Speaker voice (default: Vivian)
  --output, -o  Output .wav path (default: output.wav)
  --help, -h    Show this help
```

### Available voices

`aiden` `dylan` `eric` `ono_anna` `ryan` `serena` `sohee` `uncle_fu` `vivian`

### Examples

```bash
speak "Hello world"
speak "Good morning" -v ryan -o greeting.wav
speak "こんにちは" -v sohee -o japanese.wav
```

## How it works

1. On first run, builds a Docker image (`speak:latest`) from `nvcr.io/nvidia/pytorch:25.11-py3` with TTS dependencies pre-installed
2. Runs `generate.py` inside the container with GPU access
3. Model loads from HuggingFace cache, generates audio, writes a `.wav` file to your specified output path

Typical generation takes ~2-3s for a short sentence (RTF ~1.5x on DGX Spark).

## License

MIT
