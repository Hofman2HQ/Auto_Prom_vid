"""Text-to-speech utilities."""
from __future__ import annotations

from gtts import gTTS


def synthesize_audio(text: str, path: str) -> str:
    """Synthesize *text* to speech and save to *path*.

    Returns the path to the created audio file.
    """
    tts = gTTS(text)
    tts.save(path)
    return path
