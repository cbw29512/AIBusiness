#!/usr/bin/env python3
"""
ollama_client.py
Wrapper around the local Ollama API.
All AI generation in AIBusiness flows through this module.
"""

import json
import sys
import urllib.request
import urllib.error
from pathlib import Path
from typing import Union

ROOT = Path(__file__).parent.parent
CONFIG = json.loads((ROOT / "config.json").read_text())
OLLAMA_CFG = CONFIG["ollama"]

BASE_URL = OLLAMA_CFG["base_url"]
PREFERRED_MODELS = OLLAMA_CFG["preferred_models"]
TEMPERATURE = OLLAMA_CFG["temperature"]
TIMEOUT = OLLAMA_CFG["timeout_seconds"]


def _post(endpoint: str, payload: dict) -> dict:
    url = f"{BASE_URL}{endpoint}"
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.URLError as e:
        raise ConnectionError(
            f"Cannot reach Ollama at {BASE_URL}.\n"
            f"Make sure Ollama is running: open Terminal and run 'ollama serve'\n"
            f"Error: {e}"
        )


def _get(endpoint: str) -> dict:
    url = f"{BASE_URL}{endpoint}"
    req = urllib.request.Request(url, headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.URLError as e:
        raise ConnectionError(
            f"Cannot reach Ollama at {BASE_URL}.\n"
            f"Make sure Ollama is running: open Terminal and run 'ollama serve'\n"
            f"Error: {e}"
        )


def list_models() -> list[str]:
    """Return list of installed model names."""
    try:
        result = _get("/api/tags")
        return [m["name"] for m in result.get("models", [])]
    except ConnectionError:
        return []


def get_best_model() -> str:
    """Pick the best available model from config preferences."""
    cfg_model = OLLAMA_CFG.get("model", "auto")
    if cfg_model != "auto":
        return cfg_model

    available = list_models()
    if not available:
        raise ConnectionError(
            "No Ollama models found. Start Ollama and pull a model:\n"
            "  ollama serve\n"
            "  ollama pull llama3.2"
        )

    for preferred in PREFERRED_MODELS:
        for avail in available:
            if preferred.lower() in avail.lower():
                return avail

    return available[0]  # fallback: whatever's installed


def generate(prompt: str, system: str = "", model: str = None) -> str:
    """
    Send a prompt to Ollama and return the response text.
    Uses the best available model unless one is specified.
    """
    if model is None:
        model = get_best_model()

    payload = {
        "model": model,
        "prompt": prompt,
        "stream": False,
        "options": {
            "temperature": TEMPERATURE,
        }
    }

    if system:
        payload["system"] = system

    result = _post("/api/generate", payload)
    return result.get("response", "").strip()


def generate_json(prompt: str, system: str = "", model: str = None) -> Union[dict, list]:
    """
    Generate and parse a JSON response from Ollama.
    Retries once with explicit instruction if first parse fails.
    """
    json_system = (system + "\n\n" if system else "") + (
        "IMPORTANT: Respond with valid JSON only. No explanation, no markdown, no code fences. "
        "Start your response with { or [ and end with } or ]."
    )

    response = generate(prompt, system=json_system, model=model)

    # Strip any accidental markdown fences
    response = response.strip()
    if response.startswith("```"):
        lines = response.split("\n")
        response = "\n".join(lines[1:-1] if lines[-1].strip() == "```" else lines[1:])

    try:
        return json.loads(response)
    except json.JSONDecodeError:
        # Try to find JSON within the response
        import re
        match = re.search(r'(\{.*\}|\[.*\])', response, re.DOTALL)
        if match:
            try:
                return json.loads(match.group(1))
            except json.JSONDecodeError:
                pass
        raise ValueError(f"Ollama returned non-JSON output:\n{response[:500]}")


def check_connection() -> tuple[bool, str]:
    """Returns (ok, message) about Ollama connection status."""
    try:
        models = list_models()
        if not models:
            return False, "Ollama is running but no models are installed. Run: ollama pull llama3.2"
        model = get_best_model()
        return True, f"Connected — using model: {model} ({len(models)} model(s) available)"
    except ConnectionError as e:
        return False, str(e)


if __name__ == "__main__":
    ok, msg = check_connection()
    print(f"{'✅' if ok else '❌'} {msg}")
    if ok:
        print("\nTesting generation...")
        response = generate("Say 'hello, AIBusiness is ready' and nothing else.")
        print(f"Response: {response}")
