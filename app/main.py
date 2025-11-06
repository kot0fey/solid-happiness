from fastapi import FastAPI, UploadFile, File, Form, HTTPException, Depends
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import ValidationError
from typing import List
import os

from .models import TranscriptSegmentIn, VisitResponse
from .extractor import build_protocol_from_segments
from .quality import score_quality
from .transcription import transcribe_audio
from .utils import ensure_max_duration_and_size

app = FastAPI(title="Visit Analyzer", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------------
# ✅ Безопасность (Bearer)
# -------------------------
security = HTTPBearer()

EXPECTED_TOKEN = os.getenv("API_TOKEN", "your-token")  # можно задать через переменную окружения


def check_auth(credentials: HTTPAuthorizationCredentials = Depends(security)):
    if credentials.scheme.lower() != "bearer":
        raise HTTPException(status_code=401, detail="Invalid auth scheme")
    if credentials.credentials != EXPECTED_TOKEN:
        raise HTTPException(status_code=401, detail="Invalid or missing token")
    return True


# -------------------------
# ✅ Эндпоинты
# -------------------------

@app.post(
    "/v1/visit/analyze-transcript",
    response_model=VisitResponse,
    response_model_by_alias=True
)
async def analyze_transcript(
        segments: List[TranscriptSegmentIn],
        _: bool = Depends(check_auth)
):
    protocol = build_protocol_from_segments(segments)
    quality = score_quality(segments, protocol)
    return VisitResponse(protocol=protocol, quality=quality)


@app.post(
    "/v1/visit/analyze",
    response_model=VisitResponse,
    response_model_by_alias=True
)
async def analyze_audio(
        audio: UploadFile = File(..., description=".mp3|.wav|.m4a|.webm|.ogg, ≤30 мин, ≤100 МБ"),
        lang: str = Form("ru"),
        _: bool = Depends(check_auth)
):
    # ✅ Поддерживаемые MIME типы с учетом codecs
    allowed_mime_types = {
        "audio/mpeg", "audio/wav", "audio/x-wav", "audio/mp4", "audio/m4a",
        "audio/aac", "audio/x-m4a", "audio/webm", "video/webm", "audio/ogg",
        "audio/webm;codecs=opus", "video/webm;codecs=opus"
    }

    # ✅ Базовые MIME типы (без codecs) для проверки
    base_mime_types = {
        "audio/mpeg", "audio/wav", "audio/x-wav", "audio/mp4", "audio/m4a",
        "audio/aac", "audio/x-m4a", "audio/webm", "video/webm", "audio/ogg"
    }

    # ✅ Дополнительная проверка по расширению файла
    allowed_extensions = {'.mp3', '.wav', '.m4a', '.webm', '.ogg'}
    file_extension = os.path.splitext(audio.filename.lower())[1]

    # ✅ Проверяем MIME тип (включая codecs) И базовый MIME тип И расширение файла
    is_valid_mime = (audio.content_type in allowed_mime_types or
                     any(audio.content_type.startswith(base_type + ';') for base_type in base_mime_types))

    if not is_valid_mime and file_extension not in allowed_extensions:
        raise HTTPException(
            status_code=415,
            detail=f"Unsupported content type: {audio.content_type}. Supported: {', '.join(base_mime_types)}"
        )

    raw = await audio.read()
    ensure_max_duration_and_size(raw_bytes=raw, filename=audio.filename)

    text = transcribe_audio(raw, lang)
    if text is None:
        raise HTTPException(
            status_code=501,
            detail="Audio transcription not enabled in this build. Install faster-whisper."
        )

    segments: List[TranscriptSegmentIn] = [
        TranscriptSegmentIn(text=text, start=0, end=0, speaker="")
    ]

    protocol = build_protocol_from_segments(segments)
    quality = score_quality(segments, protocol)
    return VisitResponse(protocol=protocol, quality=quality)


# -------------------------
# ✅ Error handlers
# -------------------------

@app.exception_handler(ValidationError)
async def validation_exception_handler(request, exc: ValidationError):
    return JSONResponse(status_code=422, content={"error": "ValidationError", "details": exc.errors()})


@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc: HTTPException):
    return JSONResponse(status_code=exc.status_code, content={"error": exc.detail})