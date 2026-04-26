from pathlib import Path

from jinja2 import Environment, FileSystemLoader, select_autoescape

from .models import Card


class CardRenderer:
    """Render a Card to an HTML string using a Jinja2 template.

    A `<base href>` pointing at the template directory is injected so that
    relative asset references (CSS, fonts, icons) resolve naturally when
    the rendered HTML is loaded by the headless browser.
    """

    def __init__(self, template_dir: Path, template_name: str = "card.html.j2") -> None:
        self.template_dir = template_dir.resolve()
        self.env = Environment(
            loader=FileSystemLoader(str(self.template_dir)),
            autoescape=select_autoescape(["html"]),
            trim_blocks=True,
            lstrip_blocks=True,
        )
        self.template = self.env.get_template(template_name)

    def render(self, card: Card) -> str:
        return self.template.render(
            card=card,
            base_url=self.template_dir.as_uri() + "/",
        )
