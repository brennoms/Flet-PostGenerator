import json
import os
from .schemas import AppConfig

class ConfigManager:
    def __init__(self):
        self.config_dir = "data"
        self.config_path = os.path.join(self.config_dir, "config.json")

    def ensure_config_exists(self):
        """Checks if the config file exists; if not, creates it with defaults."""
        if not os.path.exists(self.config_dir):
            os.makedirs(self.config_dir)

        if not os.path.exists(self.config_path):
            print("Config not found. Creating default config.json...")
            default_config = AppConfig()
            self.save(default_config)

    def load(self) -> AppConfig:
        self.ensure_config_exists() 
        try:
            with open(self.config_path, "r", encoding="utf-8") as f:
                return AppConfig(**json.load(f))
        except Exception as e:
            print(f"Error loading config: {e}")
            return AppConfig()

    def save(self, config: AppConfig):
        with open(self.config_path, "w", encoding="utf-8") as f:
            f.write(config.model_dump_json(indent=4))
            