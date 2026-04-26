# Alkeymino

![Python](https://img.shields.io/badge/python-%3E%3D3.12-3776ab?logo=python&logoColor=white)
![uv](https://img.shields.io/badge/uv-managed-de5fe9?logo=python&logoColor=white)
![Playwright](https://img.shields.io/badge/rendered_by-Playwright-2ead33?logo=playwright&logoColor=white)
![Repo size](https://img.shields.io/github/repo-size/alkeymia-game/alkeymino)
![Last commit](https://img.shields.io/github/last-commit/alkeymia-game/alkeymino)
![License](https://img.shields.io/github/license/alkeymia-game/alkeymino)

Generate TCG playing-card images from a Jinja2 HTML template and YAML/JSON card data. Cards are rendered by a real headless Chromium, so the full power of CSS — gradients, custom fonts, shadows, blend modes — is available for your design.

## Features

- **Data-driven**: write a card as YAML or JSON, get a PNG.
- **Template-first**: the look lives in `templates/card.html.j2` + `card.css`. Change those, every card updates.
- **Themable**: design tokens at the top of the stylesheet plus modifier classes (`rarity-*`, `element-*`) make re-skinning trivial.
- **Batch or one-off**: render a single card or an entire folder.
- **Hi-DPI output**: 2× device scale by default (1500×2100 px from a 750×1050 viewport).

## Requirements

- Python `>= 3.12`
- [uv](https://docs.astral.sh/uv/) for dependency management
- A Chromium binary (installed once via Playwright)

## Installation

```bash
uv sync
uv run playwright install chromium
```

## Quick start

Render a single card:

```bash
uv run alkeymino examples/phoenix.yaml
```

Render every card in a folder:

```bash
uv run alkeymino examples/ -o output/
```

The generated PNGs land in `output/<card-slug>.png`.

## Card schema

A card is a flat YAML/JSON document. All fields except `name` are optional.

| Field         | Type                | Notes                                                         |
| ------------- | ------------------- | ------------------------------------------------------------- |
| `name`        | string              | Card title (required).                                        |
| `cost`        | integer             | Mana / energy cost shown in the top-left gem.                 |
| `type`        | string              | e.g. `Creature`, `Spell`, `Artifact`. Adds a `type-*` class.  |
| `subtypes`    | list of strings     | Joined with ` · ` in the type line.                           |
| `element`     | string              | `Fire`, `Water`, `Earth`, `Air`, `Aether`, `Shadow`, …        |
| `rarity`      | string              | `common`, `uncommon`, `rare`, `epic`, `legendary`.            |
| `attack`      | integer             | Shown in the bottom-right stat block (creatures only).        |
| `defense`     | integer             | Shown alongside attack — both must be set for stats to render.|
| `effect`      | string (multiline)  | Rules text. Newlines are preserved.                           |
| `flavor`      | string              | Italic flavor text below the effect.                          |
| `artwork`     | string (path / URL) | See [Artwork paths](#artwork-paths) below.                    |
| `set_code`    | string              | e.g. `ALK`.                                                   |
| `card_number` | string              | e.g. `042/200`.                                               |
| `artist`      | string              | Credited at the bottom of the card.                           |

### Artwork paths

The `artwork` field accepts three forms:

```yaml
# Relative path — resolved against the YAML file's directory (recommended).
artwork: art/phoenix.jpg

# Absolute path.
artwork: /Users/me/Pictures/phoenix.jpg

# Remote URL.
artwork: https://example.com/phoenix.jpg
```

The art frame uses `object-fit: cover`, so any aspect ratio works — the image is cropped to fit. Aim for source images that are at least as wide as the card (~750 px) for crisp output.

A recommended layout keeps art next to the card definitions:

```
examples/
├── phoenix.yaml          # artwork: art/phoenix.jpg
└── art/
    └── phoenix.jpg
```

## CLI options

```
uv run alkeymino SOURCE [OPTIONS]

  SOURCE                  Card file or directory of card files.

Options:
  -o, --output-dir PATH   Where PNGs are written.        [default: output]
  -t, --templates PATH    Template directory.            [default: templates]
      --template-name TXT Template file name.            [default: card.html.j2]
      --width INT         Viewport width in px.          [default: 750]
      --height INT        Viewport height in px.         [default: 1050]
      --scale FLOAT       Device pixel ratio.            [default: 2.0]
```

## Customizing the look

Two files control the design:

- [templates/card.html.j2](templates/card.html.j2) — semantic HTML structure (BEM classes).
- [templates/card.css](templates/card.css) — design tokens at the top, then layout, then rarity/element themes.

To re-skin everything, edit the `:root` block in `card.css`:

```css
:root {
  --color-bg: #1a1410;
  --color-frame: #2a1f17;
  --color-accent: #c9a96e;
  --font-display: "Cinzel", serif;
  --font-body: "EB Garamond", serif;
  /* … */
}
```

To add a new rarity or element, append a single rule:

```css
.rarity-mythic   { --color-accent: #ff2dd6; }
.element-arcane  { --color-accent: #6cf0ff; }
```

To preview your template without running the generator, open `templates/card.html.j2` in a browser after replacing the `{{ … }}` placeholders with sample values.

## Project structure

```
alkeymino/
├── pyproject.toml
├── src/
│   ├── main.py
│   └── alkeymino/
│       ├── models.py        # Card dataclass
│       ├── loaders.py       # YAML/JSON → Card
│       ├── renderer.py      # Card → HTML (Jinja2)
│       ├── exporter.py      # HTML → PNG (Playwright)
│       ├── generator.py     # orchestrator
│       └── cli.py           # Click CLI
├── templates/
│   ├── card.html.j2
│   └── card.css
└── examples/
    ├── phoenix.yaml
    ├── quicksilver_distillation.yaml
    └── shade_walker.yaml
```

## Programmatic use

```python
from pathlib import Path
from alkeymino import Card, CardGenerator

generator = CardGenerator(
    template_dir=Path("templates"),
    output_dir=Path("output"),
)

card = Card(
    name="Phoenix of Eternal Flame",
    cost=5,
    type="Creature",
    element="Fire",
    rarity="legendary",
    attack=4,
    defense=3,
    effect="Flying.\nReturns to your hand when destroyed.",
    artwork="examples/art/phoenix.jpg",
)

png_path = generator.generate(card)
print(png_path)
```
