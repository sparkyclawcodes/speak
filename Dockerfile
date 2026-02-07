FROM nvcr.io/nvidia/pytorch:25.11-py3
RUN pip install --no-cache-dir \
    torchaudio --index-url https://download.pytorch.org/whl/cu130
RUN pip install --no-cache-dir \
    qwen-tts soundfile onnxruntime sox
# Download and cache the model weights inside the image
RUN python -c "\
from qwen_tts import Qwen3TTSModel; \
import torch; \
m = Qwen3TTSModel.from_pretrained( \
    'Qwen/Qwen3-TTS-12Hz-1.7B-CustomVoice', \
    device_map='cpu', \
    dtype=torch.float32, \
)"
