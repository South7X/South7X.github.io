#!/usr/bin/env python3
"""Clean Loconotion output before publishing to GitHub Pages."""

from __future__ import annotations

import argparse
import re
from pathlib import Path


FIX_STYLE_ID = "github-pages-notion-fixes"
FIX_CSS = """
<style id="github-pages-notion-fixes">
html,
body,
#notion-app {
  height: auto !important;
  min-height: 100% !important;
  overflow: auto !important;
}

.notion-topbar,
.notion-print-ignore,
.notion-floating-table-of-contents,
.notion-presence-container,
.notion-overlay-container,
.notion-page-controls,
.notion-selectable-hover-menu-item {
  display: none !important;
}

.notion-frame {
  width: 100% !important;
  max-width: 100vw !important;
  height: auto !important;
  min-height: 100vh !important;
  max-height: none !important;
}

.notion-scroller {
  height: auto !important;
  max-height: none !important;
  overflow: visible !important;
}

.layout,
.layout-content {
  max-width: 100% !important;
}
</style>
""".strip()


def clean_index(index_path: Path) -> None:
    html = index_path.read_text(encoding="utf-8")

    # Loconotion can serialize missing Notion assets as literal "None" URLs.
    html = re.sub(r'<link\b[^>]*\bhref=["\']None["\'][^>]*>\s*', "", html)
    html = re.sub(r'<script\b[^>]*\bsrc=["\']None["\'][^>]*>\s*</script>\s*', "", html)

    if FIX_STYLE_ID not in html:
        html = html.replace("</head>", f"{FIX_CSS}</head>", 1)

    index_path.write_text(html, encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--site",
        default="../dist/site",
        help="Path to the Loconotion-generated site directory.",
    )
    args = parser.parse_args()

    site_dir = Path(args.site)
    index_path = site_dir / "index.html"
    if not index_path.exists():
        raise SystemExit(f"Cannot find generated index.html at {index_path}")

    clean_index(index_path)


if __name__ == "__main__":
    main()
