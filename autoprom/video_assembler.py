"""Video assembly utilities."""
from __future__ import annotations

from typing import List
from moviepy.editor import ImageClip, AudioFileClip, concatenate_videoclips


def build_video(images: List[str], audio_path: str, output_path: str, duration_per_image: float = 2.0) -> str:
    """Create a simple slideshow video from images with an audio track."""
    clips = [ImageClip(img).set_duration(duration_per_image) for img in images]
    video = concatenate_videoclips(clips, method="compose")
    audio = AudioFileClip(audio_path)
    video = video.set_audio(audio)
    video.write_videofile(output_path, fps=24)
    return output_path
