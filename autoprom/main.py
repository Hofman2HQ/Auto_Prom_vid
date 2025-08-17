"""Automated product video generator pipeline."""
from __future__ import annotations

import argparse
from pathlib import Path

from .scraper import scrape_product
from .script_generator import generate_script
from .tts import synthesize_audio
from .video_assembler import build_video


def generate_video(url: str, output: str) -> None:
    info = scrape_product(url)
    script = generate_script(info)

    output_path = Path(output)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    audio_path = str(output_path.with_suffix('.mp3'))
    synthesize_audio(script, audio_path)

    images = info.get('images', [])[:5]
    if not images:
        raise RuntimeError('No images found on product page.')

    build_video(images, audio_path, str(output_path))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate promotional product video from URL")
    parser.add_argument("url", help="Product page URL")
    parser.add_argument("output", help="Path to output MP4 file")
    args = parser.parse_args()
    generate_video(args.url, args.output)
