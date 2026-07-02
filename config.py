"""Configuration and environment variable management."""

import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv(Path(__file__).parent / ".env", override=True)

# --- TEXT GENERATION KEY (OpenRouter) ---
OPENROUTER_API_KEY: str = os.getenv("OPENROUTER_API_KEY", "")

# --- VIDEO GENERATION KEY (Hugging Face) ---
HF_API_KEY: str = os.getenv("HF_API_KEY", "")

# Free-tier text models (via OPENROUTER_API_KEY on OpenRouter)
OPENAI_TEXT_MODELS: list[str] = [
    "google/gemma-4-26b-a4b-it:free",
    "liquid/lfm-2.5-1.2b-instruct:free",
    "nvidia/nemotron-3-nano-30b-a3b:free",
    "openai/gpt-oss-20b:free",
]

# Image: Pollinations.ai — FLUX.1 (free, no key)
# No model constants needed; URL-based API

# Video: Hugging Face — damo-vilab/text-to-video-ms-1.7b (free tier available)
HF_VIDEO_MODEL: str = "damo-vilab/text-to-video-ms-1.7b"

# API endpoints
OPENROUTER_BASE_URL: str = "https://openrouter.ai/api/v1"
HF_API_BASE_URL: str = "https://api-inference.huggingface.co/models"

# Timeouts and Retries
REQUEST_TIMEOUT: int = 30
IMAGE_TIMEOUT: int = 120
VIDEO_TIMEOUT: int = 300
MAX_RETRIES: int = 2

# --- Independent key validation ---
if not OPENROUTER_API_KEY:
    raise ValueError(
        "Missing OPENROUTER_API_KEY. Required for text generation. "
        "Please set it in your .env file."
    )

# Note: HF_API_KEY is optional - free tier works without it, but has rate limits
# For production, get a free token at https://huggingface.co/settings/tokens
