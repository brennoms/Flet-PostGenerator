import pytest
from pydantic import ValidationError
from src.core.schemas import TemplateSchema, PostScale, TextAlignment

def test_template_default_values():
    """Checks if default values are correctly applied."""
    template = TemplateSchema(id=1, name="Default Test")
    assert template.scale_type == PostScale.SQUARE
    assert template.alignment == TextAlignment.CENTER
    assert template.get_effective_scale() == [1080, 1080]

def test_template_custom_scale():
    """Checks if CUSTOM scale type respects the manual scale list."""
    template = TemplateSchema(
        id=2, 
        name="Custom Test", 
        scale_type=PostScale.CUSTOM, 
        scale=[500, 500]
    )
    assert template.get_effective_scale() == [500, 500]

def test_invalid_hex_color():
    """Ensures that invalid hex colors raise a ValidationError."""
    with pytest.raises(ValidationError):
        TemplateSchema(id=3, name="Fail", bg_color="red") # Must be #HEX

def test_invalid_alignment():
    """Ensures that only left, center, and right are allowed."""
    with pytest.raises(ValidationError):
        TemplateSchema(id=4, name="Fail", alignment="top")