import pytest
from src.core.segmenter import TextSegmenter
from PIL import Image, ImageDraw, ImageFont

@pytest.fixture
def test_template():
    return {
        "id": 0,
        "name": "Test Template",
        "bg_color": "#FFFFFF",
        "font_color": "#000000",
        "font_size": 20,
        "margin": 50,
        "font_path": None  # Uses Pillow default font
    }

@pytest.fixture
def mock_tools(test_template):
    """Setup tools using the test template dimensions."""
    font = ImageFont.load_default()
    # Create a canvas based on a standard post size to simulate real drawing
    img = Image.new("RGB", (1080, 1350))
    draw = ImageDraw.Draw(img)
    return font, draw, test_template

def test_paragraph_splitting_with_template(mock_tools):
    font, draw, template = mock_tools
    text = "First paragraph.\nSecond paragraph."
    
    # Calculate constraints based on the template's margin
    max_w = 1080 - (template['margin'] * 2)
    max_h = 1350 - (template['margin'] * 2)
    
    slides = TextSegmenter.split_text_into_slides(text, max_w, max_h, font, draw)
    
    # Assertions
    assert len(slides) >= 1
    assert any("First paragraph." in line for line in slides[0])