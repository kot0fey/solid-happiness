import whisperx
from typing import List, Dict
import torch


def transcribe_audio(raw_bytes: bytes, lang: str) -> List[Dict]:
    file_path = "tmp.mp3"

    with open(file_path, "wb") as f:
        f.write(raw_bytes)

    # ✅ CPU-only
    device = "cpu"
    compute_type = "int8_float32"   # ✅ лучший режим WhisperX для CPU

    print("Using device:", device, "| compute_type:", compute_type)

    # ✅ Загружаем ASR модель (Whisper large-v2)
    model = whisperx.load_model(
        "base",
        device=device,
        compute_type=compute_type,
    )

    # ✅ транскрипция
    result = model.transcribe(file_path, language=lang)

    # ✅ Диаризация — работает на CPU автоматически
    diarize_model = whisperx.DiarizationPipeline(
        model_name="pyannote/speaker-diarization-3.1",
        device=device,
        use_auth_token=False
    )

    diarization = diarize_model(file_path)

    # ✅ объединяем слова и спикеров
    combined = whisperx.assign_word_speakers(diarization, result)

    print(combined)
    return combined

    # model = whisper.load_model("base")
    #
    #
    # result = model.transcribe(file_path, language=lang)
    # f.close()
    # print(result)
    # return result.get("text")

