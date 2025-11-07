import os
import requests
from datetime import datetime

OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.1")

LOG_FILE = "/app/llm.log"   # путь куда писать логи (можно изменить)

def write_log(message: str):
    timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"{timestamp} | {message}\n")


def call_llm(prompt: str) -> str:
    url = f"{OLLAMA_HOST}/api/generate"

    write_log(f"Sending request. Model={OLLAMA_MODEL} Host={OLLAMA_HOST} Prompt={prompt}")

    resp = requests.post(
        url,
        json={"model": OLLAMA_MODEL, "prompt": prompt, "stream": False},
        timeout=120,
    )

    write_log(f"Response raw: {resp.text}")

    resp.raise_for_status()
    data = resp.json()

    return data.get("response", "").strip()