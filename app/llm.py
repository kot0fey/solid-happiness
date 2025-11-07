import os
import json
import time
import requests

API_URL = "https://speech-analytics.qitch.ru/api/v1/prompt"
API_KEY = os.getenv("QITCH_API_KEY", "1234")

MODEL = os.getenv("QITCH_MODEL", "mistral-nemo:latest")
PROMPT_NAME = os.getenv("PROMPT_NAME", "medtech-test")


def call_llm(prompt: str) -> str:
    headers = {"X-Authorization": API_KEY}

    options = {
        "num_ctx": 15000,
        "num_predict": 4048,
        "temperature": 0,
        "top_p": 1,
        "top_k": 0,
        "repeat_penalty": 1.0,
        "seed": 42
    }

    # -------- STEP 1: GENERATE --------
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
        raise ValueError("API did not return prompt ID")

    # -------- STEP 2: POLLING --------

    result_url = f"{API_URL}/result/{prompt_id}"

    for _ in range(180):  # максимум 6 минут
        res = requests.get(result_url, headers=headers, timeout=60)
        res.raise_for_status()
        result_data = res.json()

        print("Result response:", result_data)

        status = result_data.get("status")
        result_text = result_data.get("result")

        if status == "completed" and result_text is not None:
            return result_text.strip()

        time.sleep(2)

    raise TimeoutError("LLM result polling timed out")