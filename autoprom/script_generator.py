"""Generate marketing scripts from product information."""
from __future__ import annotations

from typing import Dict


def generate_script(info: Dict[str, any]) -> str:
    """Return a simple marketing script for the given product info.

    In production this would call an LLM; for now we use a trivial template.
    """
    title = info.get("title", "Amazing Product")
    description = info.get("description", "")
    script = f"Presenting {title}! {description}"
    if not description:
        script += " Don't miss out on this fantastic item."
    return script
