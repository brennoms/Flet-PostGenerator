import pytest
from PIL import Image
from src.core.post_generator import PostGenerator
from src.core.schemas import TemplateSchema, PostScale

@pytest.fixture
def portrait_template():
    return TemplateSchema(
        id="test_1",
        name="Portrait Template",
        scale_type=PostScale.PORTRAIT,
        bg_color="#000000",
        font_color="#FFFFFF",
        font_size=40
    )

def test_generator_output_format(portrait_template):
    """Checks if the generator returns PIL Image objects with correct dimensions."""
    gen = PostGenerator(portrait_template)
    text = "Line one.\nLine two."
    
    images = gen.generate(text)
    
    assert isinstance(images, list)
    assert len(images) > 0
    assert isinstance(images[0], Image.Image)
    # Portrait should be 1080x1350
    assert images[0].size == (1080, 1350)

def test_generator_multiple_slides(portrait_template):
    """Checks if long text creates multiple images."""
    gen = PostGenerator(portrait_template)
    long_text = ("This is a long paragraph.\n" * 500)
    
    images = gen.generate(long_text)
    assert len(images) > 1

def test_background_image_loading(portrait_template, tmp_path):
    """Checks if bg_image path is handled (even if file doesn't exist)."""
    # Create a dummy image file
    bg_path = tmp_path / "bg.png"
    Image.new("RGB", (100, 100), color="blue").save(bg_path)
    
    portrait_template.bg_image = str(bg_path)
    gen = PostGenerator(portrait_template)
    
    images = gen.generate("Test")
    assert images[0].getpixel((0,0)) != (0, 0, 0) # Should not be black (default bg_color)