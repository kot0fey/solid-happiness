import os
import json
import requests

API_URL = "https://speech-analytics.qitch.ru/api/v1/prompt"
API_KEY = os.getenv("QITCH_API_KEY", "1234")

MODEL = os.getenv("QITCH_MODEL", "mistral-nemo:latest")
PROMPT_NAME = os.getenv("PROMPT_NAME", "medtech-test")


def call_llm(prompt: str) -> str:
    headers = {"X-Authorization": API_KEY}

    # ----- OPTIONS -----
    options = {
        "num_ctx": 15000,
        "num_predict": 4048,
        "temperature": 0,
        "top_p": 1,
        "top_k": 0,
        "repeat_penalty": 1.0,
        "seed": 42
    }

    # ----- STEP 1: GENERATE -----
    files = {
        "content": (None, prompt),
        "model": (None, MODEL),
        "prompt_name": (None, PROMPT_NAME),
        "options": (None, json.dumps(options)),
        "format": (None, "json")
    }

    gen = requests.post(
        f"{API_URL}/generate",
        headers=headers,
        files=files,
        timeout=120
    )
    gen.raise_for_status()

    data = gen.json()
    print("Generate response:", data)

    prompt_id = data.get("id")
    if not prompt_id:
        raise ValueError("No prompt ID returned from /generate")

    # ----- STEP 2: GET RESULT -----
    res = requests.get(
        f"{API_URL}/result/{prompt_id}",
        headers=headers,
        timeout=120
    )
    res.raise_for_status()
    result_data = res.json()

    print("Result response:", result_data)

    # сервер возвращает { id, result }
    return result_data.get("result", "").strip()