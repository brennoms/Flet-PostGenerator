import json
import os
from .schemas import TemplateSchema, TemplateFileSchema, PostScale

class TemplateManager:
    def __init__(self, storage_path="data/templates.json"):
        self.storage_path = storage_path
        self._ensure_storage_exists()

    def _ensure_storage_exists(self):
        os.makedirs(os.path.dirname(self.storage_path), exist_ok=True)
        if not os.path.exists(self.storage_path):
            default_temp = TemplateSchema(
                id=0,
                name="default",
                scale_type=PostScale.SQUARE,
                scale=[1080, 1080]
            )
            initial_data = TemplateFileSchema(next_id=1, templates=[default_temp])
            self._write_to_disk(initial_data)

    def _read_from_disk(self) -> TemplateFileSchema:
        try:
            with open(self.storage_path, "r", encoding="utf-8") as f:
                return TemplateFileSchema(**json.load(f))
        except Exception:
            return TemplateFileSchema()

    def _write_to_disk(self, data: TemplateFileSchema):
        with open(self.storage_path, "w", encoding="utf-8") as f:
            json.dump(data.model_dump(), f, indent=4)

    def load_all(self) -> list[TemplateSchema]:
        return self._read_from_disk().templates

    def add_template(self, template_data: dict):
        file_data = self._read_from_disk()
        
        template_data["id"] = file_data.next_id
        new_template = TemplateSchema(**template_data)
        
        file_data.templates.append(new_template)
        file_data.next_id += 1
        
        self._write_to_disk(file_data)
        return new_template

    def delete_template(self, template_id: int):
        file_data = self._read_from_disk()
        file_data.templates = [t for t in file_data.templates if t.id != template_id]
        self._write_to_disk(file_data)