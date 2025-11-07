import whisper
from typing import List, Dict


def transcribe_audio(raw_bytes: bytes, lang: str) -> List[Dict]:

    file_path = "tmp.mp3"
    with open(file_path, "wb") as f:
        f.write(raw_bytes)

    model = whisper.load_model("base")

    result = model.transcribe(file_path, language=lang)
    f.close()
    return result.get("text")

