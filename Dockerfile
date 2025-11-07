#FROM nvidia/cuda:12.3.2-cudnn9-runtime-ubuntu22.04
FROM pytorch/pytorch:2.8.0-cuda12.9-cudnn9-runtime
# System deps
RUN apt-get update && apt-get install -y \
    python3-pip python3 \
    ffmpeg git pkg-config \
    libavcodec-dev libavformat-dev libavdevice-dev \
    libavfilter-dev libswscale-dev libswresample-dev \
    && rm -rf /var/lib/apt/lists/*

RUN pip3 install --upgrade pip

# Torch with CUDA 12.1
RUN pip3 install torch==2.1.2 torchaudio==2.1.2 --index-url https://download.pytorch.org/whl/cu121

# whisperx + pyannote
RUN pip3 install whisperx pyannote.audio

WORKDIR /code

COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt
ENV LD_LIBRARY_PATH=/opt/conda/lib/python3.11/site-packages/nvidia/cudnn/lib:/opt/conda/lib/python3.11/site-packages/ctranslate2.libs:$LD_LIBRARY_PATH

COPY app ./app

EXPOSE 8080
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]