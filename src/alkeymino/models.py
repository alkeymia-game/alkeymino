from dataclasses import dataclass, field, fields
from typing import Any


@dataclass
class Card:
    """Data model for a single TCG card.

    Optional fields default to neutral values so partial card data
    (e.g. spells without attack/defense) renders cleanly.
    """

    name: str
    cost: int = 0
    type: str = "Creature"
    subtypes: list[str] = field(default_factory=list)
    element: str | None = None
    rarity: str = "common"
    effect: str = ""
    flavor: str = ""
    artwork: str | None = None
    attack: int | None = None
    defense: int | None = None
    set_code: str = ""
    card_number: str = ""
    artist: str = ""

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Card":
        known = {f.name for f in fields(cls)}
        unknown = set(data) - known
        if unknown:
            raise ValueError(f"Unknown card fields: {sorted(unknown)}")
        return cls(**data)
