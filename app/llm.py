import os
import requests
import logging

OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.1")
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger("LLM Client")

def call_llm(prompt: str) -> str:
    url = f"{OLLAMA_HOST}/api/generate"
    resp = requests.post(
        url,
        json={"model": OLLAMA_MODEL, "prompt": prompt, "stream": False},
        timeout=120,
    )
    logger.info(f"Model:{OLLAMA_MODEL} Host{OLLAMA_HOST} Prompt:{prompt}")
    logger.info(f"Response: {resp.json()}")
    resp.raise_for_status()
    data = resp.json()

    return data.get("response", "").strip()
