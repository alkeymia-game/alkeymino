from pathlib import Path

from .exporter import CardExporter
from .loaders import load_card
from .models import Card
from .renderer import CardRenderer


class CardGenerator:
    """Coordinator: data -> HTML -> PNG.

    Composes a renderer and an exporter so each step stays independently
    testable and replaceable (e.g. swap Playwright for WeasyPrint by
    providing a different exporter).
    """

    def __init__(
        self,
        template_dir: Path,
        output_dir: Path,
        template_name: str = "card.html.j2",
        renderer: CardRenderer | None = None,
        exporter: CardExporter | None = None,
    ) -> None:
        self.template_dir = template_dir
        self.output_dir = output_dir
        self.renderer = renderer or CardRenderer(template_dir, template_name)
        self.exporter = exporter or CardExporter()

    def generate(self, card: Card, output_name: str | None = None) -> Path:
        html = self.renderer.render(card)
        name = output_name or _slugify(card.name)
        return self.exporter.export(
            html,
            self.output_dir / f"{name}.png",
            working_dir=self.template_dir,
        )

    def generate_from_file(self, card_path: Path) -> Path:
        return self.generate(load_card(card_path), output_name=card_path.stem)


def _slugify(value: str) -> str:
    cleaned = "".join(c if c.isalnum() else "_" for c in value.strip().lower())
    return cleaned.strip("_") or "card"
