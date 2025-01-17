import json
from pathlib import Path

from nonebot import load_plugin

from canrotbot.essentials.libraries import path

_random_text_data: dict[str] = {}

for i in path.get_asset_path("random_text").glob("*.json"):
    with i.open("r", encoding="utf-8") as f:
        _random_text_data[i.stem] = json.load(f)


def get_data(name: str) -> list:
    return _random_text_data[name]


for i in Path(__file__).parent.glob("*.py"):
    if not i.stem.startswith("_"):
        load_plugin(f"canrotbot.plugins.random_text.{i.stem}")
