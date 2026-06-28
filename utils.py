"""Utility functions for the AI Content Engine."""

from datetime import datetime
from typing import Dict, Optional


def format_download_content(
    product_name: str,
    tagline: str,
    blog: str,
    social_posts: Dict[str, str],
    hero_image_url: Optional[str] = None,
    video_url: Optional[str] = None,
) -> str:
    """
    Format campaign assets into downloadable text file.

    Args:
        product_name: Name of the product
        tagline: Generated campaign tagline
        blog: Generated blog introduction
        social_posts: Dictionary with 'twitter', 'instagram', 'linkedin' keys
        hero_image_url: URL of the hero image (optional)
        video_url: URL of the promotional video (optional)

    Returns:
        str: Formatted text content ready for download
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    content = f"""AI CONTENT ENGINE - CAMPAIGN ASSETS
Generated: {timestamp}
Product: {product_name}
{'=' * 60}

TAGLINE
{'-' * 60}
{tagline}

BLOG INTRODUCTION
{'-' * 60}
{blog}

SOCIAL MEDIA POSTS
{'-' * 60}

Twitter:
{social_posts.get('twitter', 'N/A')}

Instagram:
{social_posts.get('instagram', 'N/A')}

LinkedIn:
{social_posts.get('linkedin', 'N/A')}

MEDIA ASSETS
{'-' * 60}
Hero Image URL: {hero_image_url if hero_image_url else 'N/A'}
Video URL: {video_url if video_url else 'N/A'}
"""
    return content


def validate_inputs(product_name: str, target_audience: str) -> tuple[bool, Optional[str]]:
    """
    Validate user inputs.

    Args:
        product_name: Name of the product
        target_audience: Target audience for the campaign

    Returns:
        tuple: (is_valid, error_message)
    """
    if not product_name or not product_name.strip():
        return False, "Product Name cannot be empty"

    if not target_audience or not target_audience.strip():
        return False, "Target Audience cannot be empty"

    return True, None


def format_filename(product_name: str) -> str:
    """
    Format product name for use as a safe filename.

    Replaces spaces with underscores and strips characters
    unsafe on Windows/Unix filesystems.

    Args:
        product_name: Name of the product

    Returns:
        str: Filename-safe string
    """
    import re
    safe = re.sub(r'[\\/*?:"<>|]', "", product_name)
    safe = safe.replace(" ", "_").strip("._")
    return f"{safe}_campaign.txt"
