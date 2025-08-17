from __future__ import annotations

from pathlib import Path
from typing import List
from moviepy import ImageClip, AudioFileClip, concatenate_videoclips
from PIL import Image
import requests
from io import BytesIO


def download_image(url: str) -> Image.Image:
    resp = requests.get(url, timeout=30)
    resp.raise_for_status()
    return Image.open(BytesIO(resp.content)).convert('RGB')


def build_slideshow(image_urls: List[str], audio_path: str, out_path: str, fps: int = 30) -> str:
    """Create slideshow video.

    MVP logic: equal duration per image, gentle zoom effect.
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
            continue
        w, h = img.size
        target_h = 720
        scale = target_h / h
        new_w = int(w * scale)
        img = img.resize((new_w, target_h))
        tmp_path = Path("_tmp_img.jpg")
    img.save(tmp_path)
    clip = ImageClip(str(tmp_path)).set_duration(per_image)
    # Apply gentle zoom (Ken Burns) by resizing over time
    clip = clip.fx(lambda c: c.resize(lambda t: 1 + 0.05 * (t / per_image)))
    clips.append(clip)

    if not clips:
        raise ValueError("No images could be loaded")

    video = concatenate_videoclips(clips, method='compose')
    video = video.set_audio(audio)
    video.write_videofile(out_path, fps=fps, codec='libx264', audio_codec='aac')
    return out_path

if __name__ == "__main__":
    # Example placeholder usage (needs actual audio and image urls)
    pass
