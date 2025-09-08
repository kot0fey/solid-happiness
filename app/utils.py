from fastapi import HTTPException

MAX_BYTES = 100 * 1024 * 1024  # 100 MB

def ensure_max_duration_and_size(raw_bytes: bytes, filename: str):
    if len(raw_bytes) > MAX_BYTES:
        raise HTTPException(status_code=413, detail="File too large (>100MB)")
    return True
