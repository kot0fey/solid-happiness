FROM nvidia/cuda:12.3.2-cudnn9-runtime-ubuntu22.04

RUN apt-get update && apt-get install -y \
    python3 python3-pip \
    ffmpeg git pkg-config \
    libavcodec-dev libavformat-dev libavdevice-dev \
    libavfilter-dev libswscale-dev libswresample-dev \
    && rm -rf /var/lib/apt/lists/*

RUN pip3 install --upgrade pip

# ✅ PyTorch 2.5.1 + CUDA 12.4 + cuDNN 9
RUN pip3 install torch==2.5.1 torchvision==0.20.1 torchaudio==2.5.1 --index-url https://download.pytorch.org/whl/cu124

# ✅ WhisperX + Pyannote
RUN pip3 install whisperx pyannote.audio

WORKDIR /code

COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

COPY app ./app

EXPOSE 8080

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]