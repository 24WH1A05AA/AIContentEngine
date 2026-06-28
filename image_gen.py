"""Hero image generation — uses Pollinations.ai (free, no key required)."""

import base64
import requests
from urllib.parse import quote
from typing import Dict
from config import IMAGE_TIMEOUT, MAX_RETRIES

POLLINATIONS_URL = "https://image.pollinations.ai/prompt"


class MediaAPIError(Exception):
    """Raised when image generation fails."""


class HuggingFaceImageClient:
    """
    HTTP client for image generation via Pollinations.ai (FLUX-backed, free).
    No API key required.
    """

    def generate_image(self, prompt: str) -> str:
        """
        Generate image via Pollinations.ai.

        Returns:
            str: Base64 data URI of the generated image.

        Raises:
            MediaAPIError: If generation fails after retries.
        """
        encoded = quote(prompt)
        url = f"{POLLINATIONS_URL}/{encoded}?width=1792&height=1024&nologo=true&model=flux"

        for attempt in range(MAX_RETRIES):
            try:
                response = requests.get(url, timeout=IMAGE_TIMEOUT, stream=True)
                response.raise_for_status()

                img_b64 = base64.b64encode(response.content).decode("utf-8")
                return f"data:image/jpeg;base64,{img_b64}"

            except requests.exceptions.Timeout:
                if attempt == MAX_RETRIES - 1:
                    raise MediaAPIError(
                        f"Image generation timed out after {MAX_RETRIES} attempts."
                    )
            except requests.exceptions.RequestException as e:
                if attempt == MAX_RETRIES - 1:
                    raise MediaAPIError(f"Image generation failed: {e}")


TONE_STYLE_MAP: Dict[str, Dict[str, str]] = {
    "eco": {
        "style": "watercolor painting",
        "lighting": "natural soft daylight",
        "palette": "earthy greens and browns",
    },
    "premium": {
        "style": "photorealistic",
        "lighting": "professional studio lighting with dramatic shadows",
        "palette": "luxury minimalist",
    },
    "playful": {
        "style": "bright colorful illustration",
        "lighting": "vibrant saturated lighting",
        "palette": "rainbow vivid colors",
    },
}

_client = HuggingFaceImageClient()


def build_image_prompt(product_name: str, target_audience: str, brand_tone: str) -> str:
    """Build image prompt: Subject + Style + Composition + Lighting + Constraints."""
    tone_config = TONE_STYLE_MAP.get(brand_tone.lower(), TONE_STYLE_MAP["premium"])
    return (
        f"{product_name} for {target_audience}, {tone_config['style']}, "
        f"{tone_config['lighting']}, {tone_config['palette']}, "
        f"hero shot, centered product, professional marketing image, "
        f"clean background, no text, high quality, {brand_tone} aesthetic"
    )


def generate_image(product_name: str, target_audience: str, brand_tone: str) -> str:
    """
    Generate hero image via Pollinations.ai (FLUX, free, no key required).

    Returns:
        str: Base64 data URI of the generated image.
    """
    prompt = build_image_prompt(product_name, target_audience, brand_tone)
    return _client.generate_image(prompt)
