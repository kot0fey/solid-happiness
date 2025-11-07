import whisperx
from typing import List, Dict
import torch


def transcribe_audio(raw_bytes: bytes, lang: str) -> List[Dict]:
    file_path = "tmp.mp3"

    with open(file_path, "wb") as f:
        f.write(raw_bytes)

    # 1. Определяем устройство
    device = "cuda" if torch.cuda.is_available() else "cpu"
    print("Using device:", device)
    # 2. Загружаем модель ASR
    model = whisperx.load_model("large-v2", device=device)

    # 3. Распознаём речь
    result = model.transcribe(file_path, language=lang)

    # 4. Загружаем модель диаризации (она сама использует GPU при наличии)
    diarize_model = whisperx.DiarizationPipeline(
        model_name="pyannote/speaker-diarization-3.1",
        device=device,
        use_auth_token=False
    )

    # 5. Диаризация
    diarization = diarize_model(file_path)

    # 6. Соединяем слова и спикеров
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

