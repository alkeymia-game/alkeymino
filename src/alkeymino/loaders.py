import json
from pathlib import Path
from typing import Any

import yaml

from .models import Card

_YAML_SUFFIXES = {".yaml", ".yml"}
_JSON_SUFFIXES = {".json"}
_SUPPORTED_SUFFIXES = _YAML_SUFFIXES | _JSON_SUFFIXES


def load_card(path: Path) -> Card:
    """Load a single card from a YAML or JSON file.

    Relative artwork paths are resolved against the card file's directory
    so users can keep card definitions next to their images.
    """
    data = _read_structured(path)
    _resolve_artwork(data, path.parent)
    return Card.from_dict(data)


def load_cards(directory: Path) -> list[Card]:
    """Load every supported card definition in a directory (non-recursive)."""
    return [
        load_card(p)
        for p in sorted(directory.iterdir())
        if p.is_file() and p.suffix.lower() in _SUPPORTED_SUFFIXES
    ]


def _read_structured(path: Path) -> dict[str, Any]:
    text = path.read_text(encoding="utf-8")
    suffix = path.suffix.lower()
    if suffix in _YAML_SUFFIXES:
        data = yaml.safe_load(text)
    elif suffix in _JSON_SUFFIXES:
        data = json.loads(text)
    else:
        raise ValueError(f"Unsupported card format: {path.suffix}")
    if not isinstance(data, dict):
        raise ValueError(f"{path}: expected a mapping at the top level")
    return data


def _resolve_artwork(data: dict[str, Any], base_dir: Path) -> None:
    artwork = data.get("artwork")
    if not artwork or not isinstance(artwork, str):
        return
    if artwork.startswith(("http://", "https://", "file://", "/")):
        return
    data["artwork"] = str((base_dir / artwork).resolve())
