from __future__ import annotations

from pathlib import Path
from scraper.product_scraper import scrape_product
from scriptgen.script_generator import generate_script
from tts.tts_engine import synthesize_tts
from video.video_assembler import build_slideshow
import argparse


def generate_video_from_url(url: str, workdir: str = "output", use_mock_llm: bool = True) -> str:
    Path(workdir).mkdir(parents=True, exist_ok=True)

    # 1. Scrape
    product = scrape_product(url)

    # 2. Script
    script = generate_script(product.__dict__, use_mock=use_mock_llm)
    script_path = Path(workdir) / "script.txt"
    script_path.write_text(script, encoding='utf-8')

    # 3. TTS
    audio_path = str(Path(workdir) / "voice.mp3")
    synthesize_tts(script, audio_path)

    # 4. Video
    video_path = str(Path(workdir) / "promo.mp4")
    build_slideshow(product.media.images, audio_path, video_path)

    return video_path


def main():
    parser = argparse.ArgumentParser(description="Generate promotional video from product URL")
    parser.add_argument("url", help="Product page URL")
    parser.add_argument("--out", default="output", help="Output working directory")
    parser.add_argument("--real-llm", action="store_true", help="Use real LLM (requires OPENAI_API_KEY)")
    args = parser.parse_args()

    video_path = generate_video_from_url(args.url, workdir=args.out, use_mock_llm=not args.real_llm)
    print(f"Video generated: {video_path}")


if __name__ == "__main__":
    main()
