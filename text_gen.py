"""Text content generation — uses OPENROUTER_API_KEY exclusively."""

import json
import requests
from typing import Dict
from config import (
    OPENROUTER_API_KEY,
    OPENAI_TEXT_MODELS,
    OPENROUTER_BASE_URL,
    REQUEST_TIMEOUT,
    MAX_RETRIES,
)


class TextAPIError(Exception):
    """Raised when OPENROUTER_API_KEY fails for text generation."""


class OpenAITextClient:
    """
    HTTP client for text generation.
    Uses OPENAI_API_KEY exclusively. Never used for image or video.
    """

    def __init__(self) -> None:
        assert OPENROUTER_API_KEY, (
            "OPENROUTER_API_KEY is missing. Cannot perform text generation."
        )
        self._headers = {
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json",
        }

    def complete(self, prompt: str, max_tokens: int = 500) -> str:
        """
        Call chat completions, cycling through free models with fallback.

        Raises:
            RuntimeError: If all models fail.
        """
        last_error = None

        for model in OPENAI_TEXT_MODELS:
            for attempt in range(MAX_RETRIES):
                try:
                    response = requests.post(
                        f"{OPENROUTER_BASE_URL}/chat/completions",
                        headers=self._headers,
                        json={
                            "model": model,
                            "messages": [
                                {
                                    "role": "system",
                                    "content": "You are a helpful assistant. Respond directly and concisely without showing your reasoning or thinking process.",
                                },
                                {"role": "user", "content": prompt},
                            ],
                            "max_tokens": max_tokens,
                        },
                        timeout=REQUEST_TIMEOUT,
                    )
                    if response.status_code in (429, 503):
                        last_error = f"{model}: HTTP {response.status_code}"
                        import time; time.sleep(3)
                        break  # Try next model
                    response.raise_for_status()
                    data = response.json()
                    if "choices" not in data:
                        last_error = f"{model}: unexpected response: {data.get('error', data)}"
                        break  # Try next model
                    return data["choices"][0]["message"]["content"].strip()
                except requests.exceptions.Timeout:
                    last_error = f"{model}: timeout"
                    if attempt == MAX_RETRIES - 1:
                        break
                except requests.exceptions.RequestException as e:
                    last_error = f"{model}: {e}"
                    if attempt == MAX_RETRIES - 1:
                        break

        raise TextAPIError(
            f"Text generation failed. Last error: {last_error}\n"
            "This is likely a daily free quota limit on OpenRouter. "
            "Options: wait until tomorrow (UTC midnight), add credits at "
            "https://openrouter.ai/settings/credits, or use a different API key."
        )


# Module-level client instance
_client = OpenAITextClient()


def generate_tagline(product_name: str, target_audience: str, brand_tone: str) -> str:
    """Generate campaign tagline using few-shot prompting via OPENAI_API_KEY."""
    prompt = f"""Generate a creative product tagline in {brand_tone} tone.

Examples:
- Nike: "Just Do It"
- Apple: "Think Different"
- BMW: "The Ultimate Driving Machine"

Product: {product_name}
Target Audience: {target_audience}
Tone: {brand_tone}

Rules:
- Maximum 10 words
- No hashtags
- One line only

Tagline:"""
    return _client.complete(prompt, max_tokens=50)


def generate_blog_intro(
    product_name: str, target_audience: str, brand_tone: str, tagline: str
) -> str:
    """Generate 75-word blog introduction via OPENAI_API_KEY."""
    prompt = f"""You are a Content Strategist. Write a 75-word blog introduction.

Product: {product_name}
Target Audience: {target_audience}
Brand Tone: {brand_tone}
Tagline: {tagline}

Requirements:
- Exactly 75 words
- Incorporate the tagline naturally
- Speak directly to {target_audience}
- Match {brand_tone} tone
- Engaging hook in first sentence

Blog Introduction:"""
    return _client.complete(prompt, max_tokens=150)


def generate_social_posts(
    product_name: str, target_audience: str, brand_tone: str, tagline: str
) -> Dict[str, str]:
    """Generate social media posts (Twitter, Instagram, LinkedIn) via OPENAI_API_KEY."""
    prompt = f"""Generate short social media posts in {brand_tone} tone.

Product: {product_name}
Target Audience: {target_audience}
Tagline: {tagline}

Return ONLY a JSON object with no markdown formatting:
{{
  "twitter": "Post under 150 characters, include tagline",
  "instagram": "Post under 150 characters, include tagline and 2-3 hashtags",
  "linkedin": "Post under 200 characters, professional tone, include tagline"
}}

JSON:"""
    response = _client.complete(prompt, max_tokens=250)

    # Strip markdown code fences if present, then parse JSON
    raw = response.strip()
    if "```json" in raw:
        raw = raw.split("```json")[1].split("```")[0].strip()
    elif "```" in raw:
        raw = raw.split("```")[1].split("```")[0].strip()

    try:
        return json.loads(raw)
    except json.JSONDecodeError as e:
        raise ValueError(f"Failed to parse social posts JSON: {e}\nRaw response: {raw}")
