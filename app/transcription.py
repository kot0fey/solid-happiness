import whisperx
from whisperx.diarize import DiarizationPipeline
from typing import List, Dict
import os


HF_TOKEN = os.getenv("HF_TOKEN", "your-token")  # можно задать через переменную окружения


def transcribe_audio(raw_bytes: bytes, lang: str) -> List[Dict]:
    file_path = "tmp.mp3"

    # ✅ сохраняем аудио
    with open(file_path, "wb") as f:
        f.write(raw_bytes)

    # ✅ CPU only + лучший compute_type
    device = "cpu"
    compute_type = "int8_float32"

    print("Using device:", device, "| compute_type:", compute_type)

    # ✅ Whisper ASR model
    model = whisperx.load_model(
        "base",                # можно large-v2, если хочешь лучше качество
        device=device,
        compute_type=compute_type
    )

    # ✅ Транскрипция
    result = model.transcribe(file_path, language=lang)

    # ✅ Полноценная диаризация (pyannote 3.1)
    diarize_model = DiarizationPipeline(
        model_name="pyannote/segmentation",
        device=device,
        use_auth_token=HF_TOKEN
    )

    # ✅ Диаризация
    diarization = diarize_model(file_path)

    # ✅ совмещение слов и спикеров
    combined = whisperx.assign_word_speakers(diarization, result)

    return combined