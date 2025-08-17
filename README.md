# Automated Product Video Generator

This project explores an automated pipeline to create promotional videos from
e-commerce product pages.

## Components
- **Web Scraping** – `scraper.py` collects product details and image URLs.
- **Script Generation** – `script_generator.py` builds a marketing blurb.
- **Text To Speech** – `tts.py` converts the script into spoken audio.
- **Video Assembly** – `video_assembler.py` makes a simple slideshow video.

The entry point `main.py` wires the components together. Run it with a product
URL and an output filename:

```bash
python -m autoprom.main "https://example.com/product" output.mp4
```

Additional polishing and error handling are required for production use.
