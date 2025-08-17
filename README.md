# Automated Product Promotional Video Generator (MVP)

Generate a short promotional MP4 promo video from a single e‑commerce product URL: scrape → script → voiceover → slideshow video.

## Why
Manual product video production is slow & costly. Goal: fully automated pipeline with production cost < $1 and sale price ~$5/video.

## MVP Capabilities (Current)
1. Scrape product page (title, price, description, specs, images)
2. Generate marketing script (mock copy or optional OpenAI if API key present)
3. Text‑to‑speech voiceover (Edge TTS voice if library installed; otherwise placeholder bytes)
4. Assemble slideshow video (MoviePy) with gentle zoom (Ken Burns style) and synchronized duration

## High‑Level Architecture
```
 Product URL
   │
   ▼
 [Scraper] ──> ProductData(title, price, description, specs, images)
   │
   ▼
 [Script Generator] (LLM / mock) ──> marketing script
   │
   ▼
 [TTS] Edge TTS / fallback ──> voice.mp3
   │
   ▼
 [Video Assembler] (MoviePy slideshow + zoom) ──> promo.mp4
```

## Project Structure
```
src/
  scraper/          # Web scraping logic -> ProductData dataclasses
  scriptgen/        # Prompt construction + LLM (OpenAI) integration fallback to mock
  tts/              # Text‑to‑speech abstraction (Edge TTS)
  video/            # Video assembly (image DL + MoviePy slideshow)
  pipeline.py       # Orchestrates full end‑to‑end generation + CLI main
tests/              # Basic placeholder tests
```

## Prerequisites
- Python 3.10+
- FFmpeg (required by MoviePy). On Windows install via e.g. winget or choco and ensure `ffmpeg` is in PATH.
- (Optional) Microsoft Edge TTS dependency auto‑installed (`edge-tts`) for real voices.
- (Optional) OpenAI API key for real script generation.

## Installation & Quick Start
```bash
# Create and activate virtual environment (Windows Git Bash example)
python -m venv .venv
source .venv/Scripts/activate

pip install -e .

# Generate a video with mock script (default)
auto-prom-vid "https://majorworld.com/inventory/2015-ram-1500-express-rwd/"

# Or using module path
python -m src.pipeline "https://majorworld.com/inventory/2015-ram-1500-express-rwd/"
```
Result: `output/promo.mp4` plus `script.txt` and `voice.mp3`.

### Using Real LLM Script Generation
```bash
export OPENAI_API_KEY=sk-...              # or set in .env
auto-prom-vid --real-llm <PRODUCT_URL>
```
Environment variable `PROMPT_MODEL` (default `gpt-4o-mini`) can override the model.

### CLI Options
```
auto-prom-vid URL [--out DIR] [--real-llm]
```
| Option | Description |
|--------|-------------|
| URL | Product page to scrape |
| --out DIR | Working/output directory (default: output) |
| --real-llm | Use OpenAI (requires OPENAI_API_KEY) |

## Environment Variables
| Name | Purpose | Default |
|------|---------|---------|
| OPENAI_API_KEY | Enables real script generation | (unset -> mock) |
| PROMPT_MODEL | OpenAI chat model name | gpt-4o-mini |

You may place them in a `.env` file (python-dotenv installed) if you later add loading logic.

## Cost Considerations (Planned)
- Scraping: negligible
- LLM: ~ $0.002–0.01 per script (model dependent) or $0 (mock)
- TTS: Edge voices are free (usage limits apply) or alternative TTS service cost
- Video assembly: local CPU only

Planned cost logging: track cumulative API + compute seconds per video.

## Development
```bash
pytest -q          # run basic tests
ruff check .       # lint
mypy src           # type checking
```

## Extending
- Add new scraping heuristics in `scraper/product_scraper.py`.
- Improve prompt or model selection in `scriptgen/script_generator.py`.
- Replace TTS backend by implementing a new function in `tts/tts_engine.py`.
- Enhance transitions / effects in `video/video_assembler.py`.

## Current Limitations
- Minimal error handling & retries for network calls
- No subtitle generation yet
- Single-threaded; no batching/queueing
- Image selection naive (takes up to first 12 images)
- No caching of downloaded images (re-fetches each run)
- Mock script output unless OpenAI key provided

## Roadmap (Next / Later)
Short Term:
- Subtitle generation from script (auto segmentation + burn-in)
- Image quality filtering & smart ordering
- Local image caching & hashing
- Configurable duration pacing (hero shots longer)

Medium Term:
- Multi-language voices & translated scripts
- Cost tracking & per-video report
- Basic web UI / dashboard & job queue
- Additional LLM providers (Azure OpenAI, Anthropic) abstraction

Long Term:
- AI-generated motion video segments (instead of static images)
- Brand theming (overlays, color palette, logo watermark)
- SaaS multi-tenant platform & billing integration

## Legal & Ethical Notes
Ensure you have permission to scrape & reuse media from target sites. Add robots.txt compliance & rate limiting before broad deployment.

## Contributing
1. Fork & branch: `feat/your-feature`
2. Add or update tests
3. Run lint & type checks
4. Open PR describing change & impact on cost/performance

## License
MIT (see `pyproject.toml`).

## Troubleshooting
| Issue | Fix |
|-------|-----|
| MoviePy errors about ffmpeg | Install ffmpeg & ensure on PATH (`ffmpeg -version`). |
| Empty video / no images | Target page may use JS-loaded images not yet handled. Add more scraping selectors. |
| Voice file tiny / placeholder | `edge-tts` not installed or network blocked; install dependency / check connection. |
| LLM still mock | OPENAI_API_KEY not exported or package `openai` missing. Reinstall with dependencies. |

---
This README reflects the current MVP state; functionality will expand iteratively.
