"""Configuration and environment variable management."""

import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv(Path(__file__).parent / ".env", override=True)

# --- TEXT GENERATION KEY (OpenRouter) ---
OPENROUTER_API_KEY: str = os.getenv("OPENROUTER_API_KEY", "")

# --- VIDEO GENERATION KEY (Replicate) ---
REPLICATE_API_KEY: str = os.getenv("REPLICATE_API_KEY", "")

# Free-tier text models (via OPENROUTER_API_KEY on OpenRouter)
OPENAI_TEXT_MODELS: list[str] = [
    "google/gemma-4-26b-a4b-it:free",
    "liquid/lfm-2.5-1.2b-instruct:free",
    "nvidia/nemotron-3-nano-30b-a3b:free",
    "openai/gpt-oss-20b:free",
]

# Image: Pollinations.ai — FLUX.1 (free, no key)
# No model constants needed; URL-based API

# Video models on Replicate — minimax primary, luma backup
REPLICATE_VIDEO_MODELS: dict = {
    "minimax": "minimax/video-01",
    "luma": "luma/ray-flash-2-540p",
}

# API endpoints
OPENROUTER_BASE_URL: str = "https://openrouter.ai/api/v1"
REPLICATE_BASE_URL: str = "https://api.replicate.com/v1"

# Timeouts and Retries
REQUEST_TIMEOUT: int = 30
IMAGE_TIMEOUT: int = 120
VIDEO_POLL_TIMEOUT: int = 600
MAX_RETRIES: int = 2

# --- Independent key validation ---
if not OPENROUTER_API_KEY:
    raise ValueError(
        "Missing OPENROUTER_API_KEY. Required for text generation. "
        "Please set it in your .env file."
    )

if not REPLICATE_API_KEY:
    raise ValueError(
        "Missing REPLICATE_API_KEY. Required for video generation. "
        "Get a free token at https://replicate.com and set it in your .env file."
    )
