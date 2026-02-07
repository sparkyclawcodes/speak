FROM nvcr.io/nvidia/pytorch:25.11-py3
RUN pip install --no-cache-dir \
    torchaudio --index-url https://download.pytorch.org/whl/cu130
RUN pip install --no-cache-dir \
    qwen-tts soundfile onnxruntime sox
