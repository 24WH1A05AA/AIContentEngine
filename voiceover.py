"""Voiceover generation — converts blog to speech-friendly script and MP3 audio."""

import os
import requests
import pyttsx3
from pathlib import Path
from text_gen import _client
from config import OPENROUTER_API_KEY, OPENROUTER_BASE_URL

OUTPUT_DIR = Path("voiceovers")


class VoiceoverError(Exception):
    """Raised when voiceover generation fails."""


def generate_narration_script(blog: str) -> str:
    """
    Convert blog introduction into a speech-friendly narration script.
    
    Rules:
    - Remove visual references
    - Max 15 words per sentence
    - Commas for breathing
    - Ellipses for dramatic pauses
    """
    prompt = f"""Convert this blog introduction into a speech-friendly narration script.

Rules:
- Remove any visual references like "see below", "as shown", "click here", "image shows"
- Keep sentences to maximum 15 words each
- Add commas within sentences for natural breathing points
- Use ellipses (...) for dramatic pauses or emphasis
- Write exactly as it should be spoken aloud
- Keep the same meaning and tone
- No stage directions or speaker labels
- Plain text only

Blog:
{blog}

Narration Script:"""
    return _client.complete(prompt, max_tokens=300)


def _tts_openrouter(script: str, output_path: Path) -> tuple[bool, str]:
    """Generate MP3 using local pyttsx3 engine (fallback for OpenRouter).
    
    Since OpenRouter doesn't offer direct TTS, we use pyttsx3 as a local alternative.
    This generates audio offline without requiring additional API keys.

    Returns:
        (success, reason)
    """
    try:
        # Initialize pyttsx3 engine
        engine = pyttsx3.init()
        
        # Set properties for better quality
        engine.setProperty('rate', 150)  # Speed
        engine.setProperty('volume', 0.9)  # Volume
        
        # Save to file
        engine.save_to_file(script, str(output_path))
        engine.runAndWait()
        engine.stop()
        
        return True, "ok"
    except Exception as e:
        return False, f"pyttsx3 tts failed: {e}"



def generate_voiceover(blog: str, product_name: str = "campaign") -> dict:
    """
    Convert blog to speech-friendly script and generate MP3.
    
    Uses local pyttsx3 engine for audio generation (no external API required).

    Args:
        blog: Blog introduction text
        product_name: Used for filename

    Returns:
        {
            "script": str,           # narration script
            "audio_path": str,       # path to MP3 file
        }

    Raises:
        VoiceoverError: If TTS generation fails.
    """
    script = generate_narration_script(blog)
    
    OUTPUT_DIR.mkdir(exist_ok=True)
    filename = f"{product_name}_voiceover.mp3"
    output_path = OUTPUT_DIR / filename

    ok, reason = _tts_openrouter(script, output_path)
    if ok:
        return {"script": script, "audio_path": str(output_path)}

    raise VoiceoverError(
        "Voiceover generation failed. "
        f"pyttsx3 TTS: {reason}. "
        "Ensure pyttsx3 is installed and audio system is accessible."
    )

