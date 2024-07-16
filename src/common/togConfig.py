from src.jsons.config import config_from_dict
import json


class TogConfig():
    def __init__(self) -> None:
        with open("./config/config.json", "r") as f:
            togJson = json.load(f)
            self.configJson = config_from_dict(togJson)

