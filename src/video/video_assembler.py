"""Utilities for assembling promotional videos from images and audio."""

from __future__ import annotations

from typing import List
from io import BytesIO

import numpy as np
import requests  # type: ignore[import-untyped]
from moviepy import AudioFileClip, ImageClip, concatenate_videoclips
from PIL import Image


def download_image(url: str) -> Image.Image:
    resp = requests.get(url, timeout=30)
    resp.raise_for_status()
    return Image.open(BytesIO(resp.content)).convert('RGB')


def build_slideshow(image_urls: List[str], audio_path: str, out_path: str, fps: int = 30) -> str:
    """Create a simple slideshow video from image URLs and an audio track.

    Each image is resized to 720p height, assigned an equal portion of the
    audio duration and given a subtle zoom-in effect.
    """

    audio = AudioFileClip(audio_path)
    audio_duration = audio.duration
    n = max(1, len(image_urls))
    per_image = audio_duration / n

    clips = []
    for url in image_urls:
        try:
            img = download_image(url)
        except Exception:
            # Skip images that fail to download or decode
            continue

        w, h = img.size
        target_h = 720
        scale = target_h / h
        new_w = int(w * scale)
        img = img.resize((new_w, target_h))

        # MoviePy can create clips directly from numpy arrays; avoid temp files
        frame = np.array(img)
        clip = ImageClip(frame).set_duration(per_image)
        clip = clip.fx(lambda c: c.resize(lambda t: 1 + 0.05 * (t / per_image)))
        clips.append(clip)

    if not clips:
        raise ValueError("No images could be loaded")

    video = concatenate_videoclips(clips, method="compose")
    video = video.set_audio(audio)
    video.write_videofile(out_path, fps=fps, codec="libx264", audio_codec="aac")
    return out_path

if __name__ == "__main__":
    # Example placeholder usage (needs actual audio and image urls)
    pass
