FROM python:3.11-bullseye

# ----- системные зависимости -----
RUN apt-get update && apt-get install -y \
    ffmpeg \
    git \
    libavcodec-dev \
    libavformat-dev \
    libavdevice-dev \
    libavfilter-dev \
    libswscale-dev \
    libswresample-dev \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /code

# ----- установка PyTorch совместимой версии -----
# CPU/GPU выбирается автоматически
RUN pip install --no-cache-dir torch==2.1.2 torchaudio==2.1.2 --index-url https://download.pytorch.org/whl/cpu

# ----- WhisperX + pyannote -----
RUN pip install --no-cache-dir whisperx pyannote.audio

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY app ./app

EXPOSE 8080

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080", "--log-level", "info"]
