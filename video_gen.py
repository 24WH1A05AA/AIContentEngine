"""Promotional video generation — uses REPLICATE_API_KEY exclusively."""

import time
import requests
from config import (
    REPLICATE_API_KEY,
    REPLICATE_BASE_URL,
    REPLICATE_VIDEO_MODELS,
    IMAGE_TIMEOUT,
    REQUEST_TIMEOUT,
    VIDEO_POLL_TIMEOUT,
)


class MediaAPIError(Exception):
    """Raised when REPLICATE_API_KEY fails for video generation."""


class ReplicateVideoClient:
    """
    HTTP client for video generation via Replicate.
    Uses REPLICATE_API_KEY exclusively. Never used for text or image.
    Primary: wavespeedai/wan-2.1-t2v-480p
    Backup:  genmoai/mochi-1-preview
    """

    def __init__(self) -> None:
        assert REPLICATE_API_KEY, (
            "REPLICATE_API_KEY is missing. Cannot perform video generation."
        )
        self._headers = {
            "Authorization": f"Bearer {REPLICATE_API_KEY}",
            "Content-Type": "application/json",
            "Prefer": "wait",  # wait up to 60s for result inline
        }

    def _run_model(self, model_id: str, prompt: str) -> str:
        """
        Submit prediction to Replicate and poll until complete.

        Returns:
            str: URL of the generated video.
        """
        # Create prediction
        response = requests.post(
            f"{REPLICATE_BASE_URL}/models/{model_id}/predictions",
            headers=self._headers,
            json={"input": {"prompt": prompt}},
            timeout=IMAGE_TIMEOUT,
        )
        response.raise_for_status()
        prediction = response.json()

        # If already completed (Prefer: wait)
        if prediction.get("status") == "succeeded":
            output = prediction.get("output")
            return output[0] if isinstance(output, list) else output

        prediction_id = prediction["id"]
        poll_url = f"{REPLICATE_BASE_URL}/predictions/{prediction_id}"

        # Poll for completion
        deadline = time.time() + VIDEO_POLL_TIMEOUT
        while time.time() < deadline:
            poll = requests.get(poll_url, headers=self._headers, timeout=REQUEST_TIMEOUT)
            poll.raise_for_status()
            data = poll.json()
            status = data.get("status")

            if status == "succeeded":
                output = data.get("output")
                return output[0] if isinstance(output, list) else output
            elif status == "failed":
                raise MediaAPIError(
                    f"Replicate video generation failed: {data.get('error', 'Unknown error')}"
                )

            time.sleep(5)

        raise MediaAPIError(f"Video generation exceeded {VIDEO_POLL_TIMEOUT}s timeout")

    def generate_video(self, prompt: str) -> str:
        """
        Generate video with Wan2.1 primary, CogVideoX backup.

        Returns:
            str: URL of the generated video.

        Raises:
            MediaAPIError: If all models fail.
        """
        last_error = None
        for model_key, model_id in REPLICATE_VIDEO_MODELS.items():
            try:
                return self._run_model(model_id, prompt)
            except MediaAPIError as e:
                last_error = f"{model_id}: {e}"
            except requests.exceptions.Timeout:
                last_error = f"{model_id}: timeout"
            except requests.exceptions.RequestException as e:
                last_error = f"{model_id}: {e}"

        raise MediaAPIError(
            f"Video generation failed (REPLICATE_API_KEY). Last error: {last_error}\n"
            "Check that REPLICATE_API_KEY in your .env is valid."
        )


_client = ReplicateVideoClient()


def generate_video(hero_image_url: str, product_name: str, brand_tone: str) -> str:
    """
    Generate promotional video via REPLICATE_API_KEY using Wan2.1/CogVideoX.

    Returns:
        str: URL of the generated video.
    """
    prompt = (
        f"Slow cinematic push-in on {product_name}. "
        f"Soft lighting with gentle highlights. "
        f"Minimal background movement. Professional marketing video. "
        f"Tone: {brand_tone}. High quality product showcase."
    )
    return _client.generate_video(prompt)
