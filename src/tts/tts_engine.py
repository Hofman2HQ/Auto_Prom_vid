from __future__ import annotations

import asyncio
from pathlib import Path
from typing import Optional

try:
    import edge_tts  # type: ignore
except ImportError:  # pragma: no cover
    edge_tts = None

DEFAULT_VOICE = "en-US-GuyNeural"


async def _synthesize_async(script: str, outfile: Path, voice: str = DEFAULT_VOICE) -> Path:
    if edge_tts is None:
        # fallback simple synthetic placeholder
        outfile.write_bytes(b"FAKE_WAV_DATA")
        return outfile
    communicate = edge_tts.Communicate(script, voice)
    with open(outfile, 'wb') as f:
        async for chunk in communicate.stream():  # type: ignore
            if chunk["type"] == "audio":
                f.write(chunk["data"])
    return outfile


def synthesize_tts(script: str, output_path: str, voice: str = DEFAULT_VOICE) -> str:
    """Generate speech audio file from script (MP3)."""
    out = Path(output_path)
    out.parent.mkdir(parents=True, exist_ok=True)
    try:
        asyncio.run(_synthesize_async(script, out, voice))
    except RuntimeError:
        # already in event loop (e.g., Jupyter) - use create_task
        loop = asyncio.get_event_loop()
        loop.run_until_complete(_synthesize_async(script, out, voice))
    return str(out)

if __name__ == "__main__":
    print(synthesize_tts("This is a test voice over.", "./voice.mp3"))
