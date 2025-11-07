import os
import requests
import json

API_URL = "https://speech-analytics.qitch.ru/api/v1/prompt/generate"
API_KEY = os.getenv("QITCH_API_KEY", "1234")  # как в curl

MODEL = os.getenv("QITCH_MODEL", "mistral-nemo:latest")
PROMPT_NAME = os.getenv("PROMPT_NAME", "medtech-test")

def call_llm(prompt: str) -> str:
    headers = {
        "X-Authorization": API_KEY
    }

    # Поле options должно быть строкой
    options = {
        "num_ctx": 15000,
        "num_predict": 4048,
        "temperature": 0,
        "top_p": 1,
        "top_k": 0,
        "repeat_penalty": 1.0,
        "seed": 42
    }

    # multipart/form-data → передаём в `files`
    files = {
        "content": (None, prompt),
        "model": (None, MODEL),
        "prompt_name": (None, PROMPT_NAME),
        "options": (None, json.dumps(options))
    }

    resp = requests.post(API_URL, headers=headers, files=files, timeout=300)
    resp.raise_for_status()

    data = resp.json()
    print("LLM RAW RESPONSE:", data)

    # API возвращает: { "response": "...", ... }
    return data.get("response", "").strip()