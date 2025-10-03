import json
import os
from llama_cpp import Llama

# Map model names to chat formats
CHAT_FORMATS = {
    "gemma": "gemma",
    "deepseek": "chatml",
    "mistral": "mistral-instruct",
    "llama-2": "llama-2",
    "llama2": "llama-2",
    "llama-3": "chatml",  # most llama-3 chat models use chatml
    "llama3": "chatml",
    "vicuna": "vicuna",
    "alpaca": "alpaca",
}

def detect_chat_format(model_path: str) -> str:
    """Detect chat format based on filename or folder name."""
    lower_path = model_path.lower()
    for key, fmt in CHAT_FORMATS.items():
        if key in lower_path:
            return fmt
    return None  # fallback: let llama.cpp auto-detect

def run_summarization(input_json: str, output_file: str, model_path: str):
    # Load transcript
    with open(input_json, "r", encoding="utf-8") as f:
        data = json.load(f)

    transcript = " ".join([seg["text"] for seg in data["segments"]])

    # Detect chat format
    chat_format = detect_chat_format(model_path)
    print(f"Detected chat format: {chat_format or 'auto'}")

    # Load model
    llm = Llama(
        model_path=model_path,
        n_ctx=2048,
        n_threads=os.cpu_count() or 8,
        n_gpu_layers=20,
        chat_format=chat_format  # None = auto
    )

    # Build messages
    messages = [
        {"role": "system", "content": "You are a professional newscaster."},
        {"role": "user", "content": f"Summarize this transcript into a news-style broadcast script:\n\n{transcript}"}
    ]

    # Generate
    output = llm.create_chat_completion(messages=messages, max_tokens=512, temperature=0.7)
    summary_text = output["choices"][0]["message"]["content"].strip()

    # Save
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump({"summary": summary_text}, f, indent=2)

    print(f"Summary saved to {output_file}")
