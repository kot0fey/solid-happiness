import os
import requests
import json
import time

API_URL = "https://speech-analytics.qitch.ru/api/v1/prompt/generate"
RESULT_URL = "https://speech-analytics.qitch.ru/api/v1/prompt/result"
API_KEY = os.getenv("QITCH_API_KEY", "1234")

MODEL = os.getenv("QITCH_MODEL", "mistral-nemo:latest")
PROMPT_NAME = os.getenv("PROMPT_NAME", "medtech-test")

def call_llm(prompt: str) -> str:
    headers = {
        "X-Authorization": API_KEY
    }

    options = {
        "num_ctx": 15000,
        "num_predict": 4048,
        "temperature": 0,
        "top_p": 1,
        "top_k": 0,
        "repeat_penalty": 1.0,
        "seed": 42
    }

    files = {
        "content": (None, prompt),
        "model": (None, MODEL),
        "prompt_name": (None, PROMPT_NAME),
        "options": (None, json.dumps(options))
    }

    # 1️⃣ создаём задачу
    resp = requests.post(API_URL, headers=headers, files=files, timeout=60)
    resp.raise_for_status()
    data = resp.json()
    print("LLM CREATE RESPONSE:", data)

    task_id = data["id"]

    # 2️⃣ Polling — ждём результата
    for _ in range(600):  # максимум 10 минут
        time.sleep(1)

        r = requests.get(f"{RESULT_URL}/{task_id}", headers=headers)
        r.raise_for_status()
        res = r.json()

        status = res.get("status")
        if status == "done":
            print("LLM RESULT:", res)
            return res.get("response", "")

        elif status in ("failed", "error"):
            raise RuntimeError(f"LLM failed: {res}")

        # иначе status = "processing"

    raise TimeoutError("LLM did not finish within timeout")