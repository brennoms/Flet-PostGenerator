import json
import os
from .schemas import AppConfig

class ConfigManager:
    def __init__(self, config_path="data/config.json"):
        self.config_path = config_path
        # Ensure directory exists
        os.makedirs(os.path.dirname(self.config_path), exist_ok=True)

    def load(self) -> AppConfig:
        if not os.path.exists(self.config_path):
            return AppConfig() # Returns defaults
        
        try:
            with open(self.config_path, "r", encoding="utf-8") as f:
                return AppConfig(**json.load(f))
        except Exception:
            return AppConfig()

    def save(self, config: AppConfig):
        with open(self.config_path, "w", encoding="utf-8") as f:
            f.write(config.model_dump_json(indent=4))