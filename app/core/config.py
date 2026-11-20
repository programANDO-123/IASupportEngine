import os

LLAMA_BASE_URL = os.getenv("LLAMA_BASE_URL", "http://127.0.0.1:8081").rstrip("/")
LLAMA_MODEL = os.getenv("LLAMA_MODEL", "qwen2.5-1.5b")
LLAMA_TIMEOUT_SECONDS = 150
