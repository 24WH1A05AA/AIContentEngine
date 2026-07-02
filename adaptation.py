"""Multi-channel adaptation — rewrites campaign text for specific platforms."""

import json
from typing import Dict
from text_gen import _client

CHANNELS = {
    "B2B LinkedIn": "professional B2B LinkedIn audience — use formal, ROI-focused, industry language",
    "Gen-Z TikTok": "Gen-Z TikTok audience — use casual, energetic, trendy language with slang and emojis",
    "Parents Facebook": "parents on Facebook — use warm, relatable, family-friendly language",
}


class AdaptationError(Exception):
    """Raised when channel adaptation fails."""


def adapt_for_channel(
    tagline: str,
    blog: str,
    social_posts: Dict[str, str],
    channel: str,
) -> Dict:
    """
    Rewrite tagline, blog, and social posts for the given channel.

    Args:
        tagline: Original tagline
        blog: Original blog introduction
        social_posts: Dict with twitter, instagram, linkedin keys
        channel: One of: "B2B LinkedIn", "Gen-Z TikTok", "Parents Facebook"

    Returns:
        {
            "tagline": str,
            "blog": str,
            "social": {
                "twitter": str,
                "instagram": str,
                "linkedin": str
            }
        }

    Raises:
        AdaptationError: If channel is unsupported or generation fails.
    """
    if channel not in CHANNELS:
        raise AdaptationError(
            f"Unsupported channel '{channel}'. Choose from: {', '.join(CHANNELS.keys())}"
        )

    persona = CHANNELS[channel]

    prompt = f"""You are a content adaptation specialist. Rewrite the marketing campaign for {persona}.

Original Tagline:
{tagline}

Original Blog:
{blog}

Original Social Posts:
{json.dumps(social_posts)}

Rewrite all three assets for the {channel} channel while keeping the same product meaning.

Return ONLY this JSON:
{{
  "tagline": "adapted tagline (max 10 words)",
  "blog": "adapted blog introduction (~75 words)",
  "social": {{
    "twitter": "adapted Twitter post",
    "instagram": "adapted Instagram post with hashtags",
    "linkedin": "adapted LinkedIn post"
  }}
}}

JSON:"""

    response = _client.complete(prompt, max_tokens=600)
    raw = response.strip()
    if "```json" in raw:
        raw = raw.split("```json")[1].split("```")[0].strip()
    elif "```" in raw:
        raw = raw.split("```")[1].split("```")[0].strip()

    try:
        return json.loads(raw)
    except json.JSONDecodeError as e:
        raise AdaptationError(f"Failed to parse adaptation JSON: {e}\nRaw: {raw}")
