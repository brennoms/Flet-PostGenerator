import textwrap

class TextSegmenter:
    @staticmethod
    def get_chars_per_line(max_width, font, draw):
        """Calculates the average number of characters that fit within the given width."""
        avg_char_width = draw.textlength("a", font=font)
        return int(max_width / avg_char_width)

    @staticmethod
    def split_text_into_slides(text, max_width, max_height, font, draw):
        """Divides text into slides, ensuring paragraphs are not split across images."""
        
        # 1. Setup dimensions
        chars_per_line = TextSegmenter.get_chars_per_line(max_width, font, draw)
        bbox = draw.textbbox((0, 0), "Ay", font=font)
        line_height = (bbox[3] - bbox[1]) + 15
        max_lines_per_slide = int(max_height / line_height)

        # 2. Split input into raw paragraphs
        raw_paragraphs = text.split('\n')
        
        slides = []
        current_slide_lines = []

        for para in raw_paragraphs:
            para = para.strip()
            if not para:
                continue
            
            # Wrap the specific paragraph into lines
            para_lines = textwrap.wrap(para, width=chars_per_line, break_long_words=False)
            
            # Check if this paragraph is too long even for a blank slide
            if len(para_lines) > max_lines_per_slide:
                # If a single paragraph is larger than a slide, we must break it 
                # to avoid an infinite loop or missing text
                chunks = [para_lines[i:i + max_lines_per_slide] for i in range(0, len(para_lines), max_lines_per_slide)]
                
                # Close current slide if it has content
                if current_slide_lines:
                    slides.append(current_slide_lines)
                    current_slide_lines = []
                
                # Add the chunks as full slides
                slides.extend(chunks[:-1])
                current_slide_lines = chunks[-1]
            
            # Check if paragraph fits in the current slide
            elif len(current_slide_lines) + len(para_lines) <= max_lines_per_slide:
                current_slide_lines.extend(para_lines)
            
            else:
                # Slide is full, save it and start a new one with the current paragraph
                slides.append(current_slide_lines)
                current_slide_lines = para_lines

        # 3. Add the last slide if not empty
        if current_slide_lines:
            slides.append(current_slide_lines)

        return slides