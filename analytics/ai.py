import os
import logging

logger = logging.getLogger(__name__)

API_MODEL = "gpt-4"

try:
    from openai import OpenAI
    _client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
except ImportError:
    _client = None
    logger.warning("openai package not installed")


def predict_sales(prompt: str) -> str:
    if _client is None:
        return "Sales prediction not available (openai not installed)"
    response = _client.chat.completions.create(
        model=API_MODEL,
        messages=[{"role": "user", "content": prompt}],
    )
    return response.choices[0].message.content


def detect_irregularities(data: str) -> str:
    if _client is None:
        return "Irregularity analysis not available (openai not installed)"
    prompt = f"Detect irregularities in: {data}"
    response = _client.chat.completions.create(
        model=API_MODEL,
        messages=[{"role": "user", "content": prompt}],
    )
    return response.choices[0].message.content
