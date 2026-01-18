from enum import Enum
from typing import Optional, List, Union
from pydantic import BaseModel, Field

class TextAlignment(str, Enum):
    LEFT = "left"
    CENTER = "center"
    RIGHT = "right"

class PostScale(str, Enum):
    SQUARE = "square"           # [1080, 1080]
    PORTRAIT = "portrait"       # [1080, 1350]
    VERTICAL = "vertical"       # [1080, 1920]
    CUSTOM = "custom"

# Map for internal use
SCALE_MAP = {
    PostScale.SQUARE: [1080, 1080],
    PostScale.PORTRAIT: [1080, 1350],
    PostScale.VERTICAL: [1080, 1920],
}

class TemplateSchema(BaseModel):
    id: Union[int, str]
    name: str
    scale_type: PostScale = Field(default=PostScale.SQUARE)
    scale: List[int] = Field(default=[1080, 1080], min_items=2, max_items=2)
    bg_color: str = Field(default="#FFFFFF", pattern=r'^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$')
    bg_image: Optional[str] = None
    font_color: str = Field(default="#000000", pattern=r'^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$')
    font_size: int = Field(default=42, gt=0)
    font_path: Optional[str] = None
    alignment: TextAlignment = Field(default=TextAlignment.CENTER)
    margin: int = Field(default=50, ge=0)

    def get_effective_scale(self) -> List[int]:
        if self.scale_type == PostScale.CUSTOM:
            return self.scale
        return SCALE_MAP.get(self.scale_type, [1080, 1080])

class TemplateFileSchema(BaseModel):
    next_id: int = 1
    templates: List[TemplateSchema] = []

class AppConfig(BaseModel):
    working_directory: Optional[str] = None
    last_used_template_id: Union[int, str] = 0
    theme_mode: str = "dark"  # dark, light, system
    auto_open_folder: bool = True
