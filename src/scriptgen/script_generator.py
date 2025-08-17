from __future__ import annotations

from typing import Dict
from textwrap import dedent
import os

try:
    from openai import OpenAI  # type: ignore
except ImportError:  # pragma: no cover
    OpenAI = None  # type: ignore

BASIC_MARKETING_TEMPLATE = dedent(
    """
    Create a concise upbeat 60-90 second promotional script for a product video.
    Use the following structured data:
    Title: {title}
    Price: {price}
    Key Specs:
    {spec_lines}
    Description: {description}

    Guidelines:
    - Hook in first sentence.
    - Highlight 4-6 most compelling specs (avoid listing too many numbers).
    - Use persuasive, energetic but credible tone.
    - Include a soft call to action at end (e.g., Visit the link to learn more.).
    - Keep under 180 words.
    Provide ONLY the script lines, no intro labels.
    """.strip()
)


def build_prompt(product: Dict) -> str:
    spec_lines = "\n".join(f"- {k}: {v}" for k, v in list(product.get('specs', {}).items())[:12])
    return BASIC_MARKETING_TEMPLATE.format(
        title=product.get('title','Product'),
        price=product.get('price','N/A'),
        spec_lines=spec_lines or "- (No structured specs extracted)",
        description=product.get('description','')[:600]
    )


def mock_llm_generate(product: Dict) -> str:
    """Fallback script generation without external LLM calls.

    Creates a basic marketing message using available product fields so tests
    and offline usage still yield meaningful output.
    """

    title = product.get("title", "this product")
    price = product.get("price")
    price_line = f"Priced at {price}, " if price else ""
    description = product.get("description", "")
    first_spec = next(iter(product.get("specs", {}).items()), None)
    spec_line = f"It features {first_spec[0]} {first_spec[1]}. " if first_spec else ""

    return (
        f"Introducing {title}! {price_line}{spec_line}{description[:80]} "
        "Visit the link to learn more."
    )


def generate_script(product: Dict, use_mock: bool = True) -> str:
    """Generate marketing script.

    If use_mock is False and OPENAI_API_KEY is present, attempts real LLM call.
    Falls back to mock on any error.
    """
    prompt = build_prompt(product)
    if use_mock:
        return mock_llm_generate(product)

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key or OpenAI is None:
        return mock_llm_generate(product)
    try:
        client = OpenAI()
        model = os.getenv("PROMPT_MODEL", "gpt-4o-mini")
        resp = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are a marketing copywriter."},
                {"role": "user", "content": prompt},
            ],
            temperature=0.7,
            max_tokens=320,
        )
        text = resp.choices[0].message.content if resp.choices else None  # type: ignore
        if not text:
            return mock_llm_generate(product)
        return text.strip()
    except Exception:
        return mock_llm_generate(product)

if __name__ == "__main__":
    sample = {"title": "Sample Car", "price":"$19,995", "specs": {"Engine":"V6"}, "description":"A reliable vehicle."}
    print(generate_script(sample))
