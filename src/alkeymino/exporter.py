import tempfile
from pathlib import Path

from playwright.sync_api import sync_playwright


class CardExporter:
    """Render an HTML string to a PNG using a headless Chromium.

    The HTML is written to a temp file inside `working_dir` so the
    document loads from a `file://` origin — Chromium blocks `file://`
    assets (CSS, fonts, images) when the page itself is served from a
    non-`file://` origin like `about:blank`.
    """

    def __init__(
        self,
        width: int = 750,
        height: int = 1050,
        scale: float = 2.0,
        selector: str = ".card",
    ) -> None:
        self.width = width
        self.height = height
        self.scale = scale
        self.selector = selector

    def export(self, html: str, output_path: Path, working_dir: Path) -> Path:
        output_path = output_path.resolve()
        output_path.parent.mkdir(parents=True, exist_ok=True)

        with tempfile.NamedTemporaryFile(
            mode="w",
            encoding="utf-8",
            suffix=".html",
            prefix="_alkeymino_",
            dir=str(working_dir),
            delete=False,
        ) as tmp:
            tmp.write(html)
            tmp_path = Path(tmp.name)

        try:
            with sync_playwright() as p:
                browser = p.chromium.launch()
                try:
                    context = browser.new_context(
                        viewport={"width": self.width, "height": self.height},
                        device_scale_factor=self.scale,
                    )
                    page = context.new_page()
                    page.goto(tmp_path.as_uri(), wait_until="networkidle")
                    page.locator(self.selector).screenshot(
                        path=str(output_path),
                        omit_background=True,
                    )
                finally:
                    browser.close()
        finally:
            tmp_path.unlink(missing_ok=True)

        return output_path
