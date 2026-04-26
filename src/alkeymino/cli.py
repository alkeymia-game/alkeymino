from pathlib import Path

import click

from .exporter import CardExporter
from .generator import CardGenerator
from .renderer import CardRenderer

_PROJECT_ROOT = Path(__file__).resolve().parents[2]
_DEFAULT_TEMPLATES = _PROJECT_ROOT / "templates"
_SUPPORTED_SUFFIXES = {".yaml", ".yml", ".json"}


@click.command()
@click.argument(
    "source",
    type=click.Path(exists=True, path_type=Path, file_okay=True, dir_okay=True),
)
@click.option(
    "-o", "--output-dir",
    type=click.Path(path_type=Path, file_okay=False),
    default=Path("output"),
    show_default=True,
    help="Directory where PNGs are written.",
)
@click.option(
    "-t", "--templates",
    type=click.Path(exists=True, path_type=Path, file_okay=False),
    default=_DEFAULT_TEMPLATES,
    show_default=True,
    help="Directory containing the Jinja2 template and CSS.",
)
@click.option(
    "--template-name",
    default="card.html.j2",
    show_default=True,
    help="Template file name inside the templates directory.",
)
@click.option("--width", type=int, default=750, show_default=True)
@click.option("--height", type=int, default=1050, show_default=True)
@click.option("--scale", type=float, default=2.0, show_default=True)
def main(
    source: Path,
    output_dir: Path,
    templates: Path,
    template_name: str,
    width: int,
    height: int,
    scale: float,
) -> None:
    """Generate card PNGs from a YAML/JSON file or a directory of them."""
    generator = CardGenerator(
        template_dir=templates,
        output_dir=output_dir,
        renderer=CardRenderer(templates, template_name),
        exporter=CardExporter(width=width, height=height, scale=scale),
    )

    targets = _collect_targets(source)
    if not targets:
        raise click.UsageError(f"No card files found in {source}")

    for path in targets:
        result = generator.generate_from_file(path)
        click.echo(f"[ok] {path.name} -> {result}")


def _collect_targets(source: Path) -> list[Path]:
    if source.is_file():
        return [source]
    return sorted(
        p for p in source.iterdir()
        if p.is_file() and p.suffix.lower() in _SUPPORTED_SUFFIXES
    )


if __name__ == "__main__":
    main()
