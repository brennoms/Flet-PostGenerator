from PIL import Image, ImageDraw, ImageFont
import os
from .segmenter import TextSegmenter
from .schemas import TemplateSchema, TextAlignment

class PostGenerator:
    """
    Handles the visual rendering of social media posts using Pillow,
    based on templates and segmented text.
    """
    
    def __init__(self, template: TemplateSchema):
        self.template = template
        self.width, self.height = self.template.get_effective_scale()
        self.margin = self.template.margin

    def _get_font(self) -> ImageFont.FreeTypeFont:
        """Loads the configured font or falls back to the default system font."""
        try:
            if self.template.font_path and os.path.exists(self.template.font_path):
                return ImageFont.truetype(self.template.font_path, self.template.font_size)
            return ImageFont.load_default()
        except Exception:
            return ImageFont.load_default()

    def generate(self, text: str) -> list[Image.Image]:
        """
        Main entry point: segments text and renders a list of PIL Images.
        """
        font = self._get_font()
        
        # We need a dummy image and draw object just to measure text during segmentation
        dummy_img = Image.new("RGB", (1, 1))
        dummy_draw = ImageDraw.Draw(dummy_img)

        # Calculate usable area for text
        max_w = self.width - (self.margin * 2)
        max_h = self.height - (self.margin * 2)

        # Call the segmenter logic to get pages (slides) of text
        slides_content = TextSegmenter.split_text_into_slides(
            text, max_w, max_h, font, dummy_draw
        )

        # Render each slide
        return [self._render_slide(lines, font) for lines in slides_content]

    def _render_slide(self, lines: list[str], font: ImageFont.FreeTypeFont) -> Image.Image:
        """Renders a single image slide with background and aligned text."""
        
        # 1. Background setup
        if self.template.bg_image and os.path.exists(self.template.bg_image):
            img = Image.open(self.template.bg_image).convert("RGB")
            img = img.resize((self.width, self.height), Image.Resampling.LANCZOS)
        else:
            img = Image.new("RGB", (self.width, self.height), color=self.template.bg_color)
        
        draw = ImageDraw.Draw(img)

        # 2. Vertical Centering Calculation
        # We calculate the total height of the text block to center it as a whole
        ascent, descent = font.getmetrics()
        line_height = ascent + descent + 15 # text height + line spacing
        total_text_height = len(lines) * line_height
        
        current_y = (self.height - total_text_height) // 2

        # 3. Draw each line with horizontal alignment
        for line in lines:
            line_w = draw.textlength(line, font=font)
            
            if self.template.alignment == TextAlignment.CENTER:
                current_x = (self.width - line_w) // 2
            elif self.template.alignment == TextAlignment.RIGHT:
                current_x = self.width - line_w - self.margin
            else: # LEFT
                current_x = self.margin

            draw.text(
                (current_x, current_y), 
                line, 
                font=font, 
                fill=self.template.font_color
            )
            current_y += line_height

        return img
