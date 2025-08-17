from scraper.product_scraper import ProductData
from scriptgen.script_generator import generate_script


def test_generate_script_mock():
    product = ProductData(
        url="https://example.com/item",
        title="Test Widget",
        price="$19.99",
        description="A versatile widget for everyday tasks.",
        specs={"Weight": "1kg", "Color": "Red"},
        media=None,  # not needed for script
    ).__dict__
    script = generate_script(product, use_mock=True)
    assert isinstance(script, str) and len(script) > 10
