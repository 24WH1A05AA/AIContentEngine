"""Promotional video generation — uses Hugging Face Inference API for AI video generation."""

import os
import requests
from pathlib import Path
from config import IMAGE_TIMEOUT, REQUEST_TIMEOUT, HF_API_KEY, HF_VIDEO_MODEL, HF_API_BASE_URL, VIDEO_TIMEOUT

OUTPUT_DIR = Path("generated_videos")


class MediaAPIError(Exception):
    """Raised when video generation fails."""


class HuggingFaceVideoClient:
    """
    HTTP client for AI video generation via Hugging Face Inference API.
    Uses HF_API_KEY for video generation.
    Model: damo-vilab/text-to-video-ms-1.7b (free tier available)
    """

    def __init__(self) -> None:
        self.api_key = HF_API_KEY
        self.api_url = f"{HF_API_BASE_URL}/{HF_VIDEO_MODEL}"
        
    def _get_headers(self) -> dict:
        """Get request headers with API key if available."""
        headers = {"Content-Type": "application/json"}
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"
        return headers

    def generate_video(self, prompt: str) -> str:
        """
        Generate video via Hugging Face Inference API.
        
        Model: damo-vilab/text-to-video-ms-1.7b
        - Free tier: 30 calls/minute
        - High quality video generation
        - No rate limiting issues like Replicate

        Returns:
            str: URL or local path of the generated video.

        Raises:
            MediaAPIError: If generation fails.
        """
        try:
            headers = self._get_headers()
            
            # Request video generation
            payload = {"inputs": prompt}
            
            response = requests.post(
                self.api_url,
                headers=headers,
                json=payload,
                timeout=VIDEO_TIMEOUT,
            )
            
            # Check response status
            if response.status_code == 503:
                raise MediaAPIError(
                    "Hugging Face model is loading. Model will be ready in a moment. Please try again."
                )
            elif response.status_code == 529:
                raise MediaAPIError(
                    "Hugging Face service temporarily overloaded. Please try again in a minute."
                )
            elif response.status_code == 401:
                raise MediaAPIError(
                    "HF_API_KEY is invalid. Get a free token at https://huggingface.co/settings/tokens"
                )
            
            response.raise_for_status()
            
            # Hugging Face returns binary video content
            OUTPUT_DIR.mkdir(exist_ok=True)
            video_path = OUTPUT_DIR / "generated_video.mp4"
            
            with open(video_path, "wb") as f:
                f.write(response.content)
            
            return str(video_path)
            
        except requests.exceptions.Timeout:
            raise MediaAPIError("Video generation timed out. Hugging Face model processing took too long. Try again.")
        except requests.exceptions.RequestException as e:
            if "401" in str(e) or "unauthorized" in str(e).lower():
                raise MediaAPIError(
                    "HF_API_KEY is invalid or missing. "
                    "Get a free token at https://huggingface.co/settings/tokens"
                )
            raise MediaAPIError(f"Video generation failed: {e}")
        except Exception as e:
            raise MediaAPIError(f"Unexpected error during video generation: {e}")


_client = HuggingFaceVideoClient()


def generate_video(hero_image_url: str, product_name: str, brand_tone: str) -> str:
    """
    Generate promotional video via Hugging Face AI models.
    
    Uses: damo-vilab/text-to-video-ms-1.7b (free tier available)
    
    Args:
        hero_image_url: Image URL (for reference, not used in generation)
        product_name: Product name for video context
        brand_tone: Brand tone/style for video

    Returns:
        str: Path to the generated video file.

    Raises:
        MediaAPIError: If video generation fails.
    """
    prompt = (
        f"Professional marketing video for {product_name}. "
        f"Slow cinematic product showcase with gentle lighting. "
        f"Smooth camera movement, clean background. "
        f"Style: {brand_tone}. "
        f"High quality, professional production."
    )
    return _client.generate_video(prompt)
