import whisperx
from whisperx.diarize import DiarizationPipeline
from typing import List, Dict

def transcribe_audio(raw_bytes: bytes, lang: str) -> List[Dict]:
    file_path = "tmp.mp3"

    with open(file_path, "wb") as f:
        f.write(raw_bytes)

    device = "cpu"
    compute_type = "int8_float32"

    print("Using device:", device)

    model = whisperx.load_model(
        "base",
        device=device,
        compute_type=compute_type
    )

    result = model.transcribe(file_path, language=lang)

    # ✅ бесплатная модель сегментации вместо диаризации 3.1
    diarize_model = DiarizationPipeline(
        model_name="pyannote/segmentation",
        device=device,
        use_auth_token=False
    )

    diarization = diarize_model(file_path)

    combined = whisperx.assign_word_speakers(diarization, result)

    return combined