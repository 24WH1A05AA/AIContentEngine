"""AI self-critique — evaluates campaign content quality."""

import json
from typing import Dict
from text_gen import _client


def _evaluate_asset(asset_name: str, content: str, product_name: str, target_audience: str, brand_tone: str) -> Dict:
    """
    Evaluate a single asset against quality criteria.
    
    Returns:
        {"pass": bool, "issue": str | None}
    """
    prompt = f"""You are a marketing content quality reviewer.

Evaluate this {asset_name} for a marketing campaign.

Product: {product_name}
Target Audience: {target_audience}
Brand Tone: {brand_tone}

Content to evaluate:
{content}

Evaluate against these criteria:
- Tone matches "{brand_tone}" brand voice
- Speaks to "{target_audience}" audience
- Appropriate length for {asset_name}
- Mentions or relates to "{product_name}"

Return ONLY a JSON object:
{{"pass": true, "issue": null}}
or
{{"pass": false, "issue": "brief reason"}}

JSON:"""
    response = _client.complete(prompt, max_tokens=60)
    raw = response.strip()
    if "```json" in raw:
        raw = raw.split("```json")[1].split("```")[0].strip()
    elif "```" in raw:
        raw = raw.split("```")[1].split("```")[0].strip()
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        return {"pass": True, "issue": None}


def _regenerate_tagline(product_name: str, target_audience: str, brand_tone: str, feedback: str) -> str:
    """Regenerate tagline with critic feedback injected."""
    prompt = f"""Generate a creative product tagline in {brand_tone} tone.

Product: {product_name}
Target Audience: {target_audience}
Tone: {brand_tone}

IMPORTANT: Address this feedback from the previous attempt:
{feedback}

Rules:
- Maximum 10 words
- No hashtags
- One line only

Tagline:"""
    return _client.complete(prompt, max_tokens=50)


def _regenerate_blog(product_name: str, target_audience: str, brand_tone: str, tagline: str, feedback: str) -> str:
    """Regenerate blog with critic feedback injected."""
    prompt = f"""You are a Content Strategist. Write a 75-word blog introduction.

Product: {product_name}
Target Audience: {target_audience}
Brand Tone: {brand_tone}
Tagline: {tagline}

IMPORTANT: Address this feedback from the previous attempt:
{feedback}

Requirements:
- Exactly 75 words
- Incorporate the tagline naturally
- Speak directly to {target_audience}
- Match {brand_tone} tone
- Engaging hook in first sentence

Blog Introduction:"""
    return _client.complete(prompt, max_tokens=150)


def _regenerate_social(product_name: str, target_audience: str, brand_tone: str, tagline: str, feedback: str) -> Dict[str, str]:
    """Regenerate social posts with critic feedback injected."""
    prompt = f"""Generate short social media posts in {brand_tone} tone.

Product: {product_name}
Target Audience: {target_audience}
Tagline: {tagline}

IMPORTANT: Address this feedback from the previous attempt:
{feedback}

Return ONLY a JSON object with no markdown formatting:
{{
  "twitter": "Post under 150 characters, include tagline",
  "instagram": "Post under 150 characters, include tagline and 2-3 hashtags",
  "linkedin": "Post under 200 characters, professional tone, include tagline"
}}

JSON:"""
    response = _client.complete(prompt, max_tokens=250)
    raw = response.strip()
    if "```json" in raw:
        raw = raw.split("```json")[1].split("```")[0].strip()
    elif "```" in raw:
        raw = raw.split("```")[1].split("```")[0].strip()
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        return {"twitter": "", "instagram": "", "linkedin": ""}


def critique(
    tagline: str,
    blog: str,
    social_posts: Dict[str, str],
    product_name: str,
    target_audience: str,
    brand_tone: str,
) -> Dict:
    """
    Evaluate tagline, blog, and social posts for quality.

    Args:
        tagline: Campaign tagline
        blog: Blog introduction text
        social_posts: Dict with twitter, instagram, linkedin keys
        product_name: Product name
        target_audience: Target audience
        brand_tone: Brand tone

    Returns:
        {
            "tagline": {"pass": bool, "issue": str | None},
            "blog": {"pass": bool, "issue": str | None},
            "social": {"pass": bool, "issue": str | None}
        }
    """
    return {
        "tagline": _evaluate_asset("tagline", tagline, product_name, target_audience, brand_tone),
        "blog": _evaluate_asset("blog introduction", blog, product_name, target_audience, brand_tone),
        "social": _evaluate_asset("social media posts", json.dumps(social_posts), product_name, target_audience, brand_tone),
    }


def critique_and_regenerate(
    tagline: str,
    blog: str,
    social_posts: Dict[str, str],
    product_name: str,
    target_audience: str,
    brand_tone: str,
) -> Dict:
    """
    Critique content and regenerate failed assets with feedback injection.
    Maximum 2 retries per asset.

    Returns:
        {
            "tagline": {"content": str, "pass": bool, "issue": str | None, "retries": int},
            "blog": {"content": str, "pass": bool, "issue": str | None, "retries": int},
            "social": {"content": Dict, "pass": bool, "issue": str | None, "retries": int},
            "warning": bool
        }
    """
    report = {}
    warning = False

    # --- Regenerate tagline if failing ---
    retries = 0
    result = _evaluate_asset("tagline", tagline, product_name, target_audience, brand_tone)
    while not result["pass"] and retries < 2:
        retries += 1
        tagline = _regenerate_tagline(product_name, target_audience, brand_tone, result["issue"])
        result = _evaluate_asset("tagline", tagline, product_name, target_audience, brand_tone)
    report["tagline"] = {
        "content": tagline,
        "pass": result["pass"],
        "issue": result["issue"],
        "retries": retries,
    }
    if not result["pass"]:
        warning = True

    # --- Regenerate blog if failing ---
    retries = 0
    result = _evaluate_asset("blog introduction", blog, product_name, target_audience, brand_tone)
    while not result["pass"] and retries < 2:
        retries += 1
        blog = _regenerate_blog(product_name, target_audience, brand_tone, tagline, result["issue"])
        result = _evaluate_asset("blog introduction", blog, product_name, target_audience, brand_tone)
    report["blog"] = {
        "content": blog,
        "pass": result["pass"],
        "issue": result["issue"],
        "retries": retries,
    }
    if not result["pass"]:
        warning = True

    # --- Regenerate social if failing ---
    retries = 0
    social_str = json.dumps(social_posts)
    result = _evaluate_asset("social media posts", social_str, product_name, target_audience, brand_tone)
    while not result["pass"] and retries < 2:
        retries += 1
        social_posts = _regenerate_social(product_name, target_audience, brand_tone, tagline, result["issue"])
        social_str = json.dumps(social_posts)
        result = _evaluate_asset("social media posts", social_str, product_name, target_audience, brand_tone)
    report["social"] = {
        "content": social_posts,
        "pass": result["pass"],
        "issue": result["issue"],
        "retries": retries,
    }
    if not result["pass"]:
        warning = True

    report["warning"] = warning
    return report
