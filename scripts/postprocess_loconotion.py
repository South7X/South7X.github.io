#!/usr/bin/env python3
"""Clean Loconotion output before publishing to GitHub Pages."""

from __future__ import annotations

import argparse
import re
from pathlib import Path


FIX_STYLE_ID = "github-pages-notion-fixes"
FIX_CSS = """
<style id="github-pages-notion-fixes">
:root {
  --page-max-width: 1600px;
  --page-inline-padding: clamp(24px, 4vw, 64px);
  --profile-column-width: clamp(260px, 22vw, 320px);
  --profile-column-gap: clamp(28px, 4vw, 56px);
}

html,
body,
#notion-app {
  width: 100% !important;
  height: auto !important;
  min-height: 100% !important;
  max-width: 100% !important;
  overflow-x: hidden !important;
  overflow-y: auto !important;
}

body {
  position: static !important;
}

#notion-app,
.notion-light-theme,
.notion-app-inner,
.notion-app-inner > div,
.notion-cursor-listener,
.notion-cursor-listener > div {
  width: 100% !important;
  height: auto !important;
  min-height: 100% !important;
  max-width: 100% !important;
  overflow: visible !important;
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
  width: 100% !important;
  height: auto !important;
  max-height: none !important;
  overflow: visible !important;
}

.whenContentEditable,
.layout,
.layout-full,
.layout-content,
.layout-content > div,
.layout-content > div > div {
  width: min(100%, var(--page-max-width)) !important;
  max-width: 100% !important;
  box-sizing: border-box !important;
}

.layout {
  display: block !important;
  margin-inline: auto !important;
  padding-inline: var(--page-inline-padding) !important;
  padding-bottom: clamp(40px, 8vh, 96px) !important;
}

.layout-content {
  margin-inline: auto !important;
}

.notion-selectable {
  max-width: 100% !important;
}

.notion-column_list-block > div {
  width: 100% !important;
  align-items: flex-start !important;
}

.notion-column_list-block > div > div:first-child {
  width: var(--profile-column-width) !important;
  flex: 0 0 var(--profile-column-width) !important;
}

.notion-column_list-block > div > div:nth-child(2) {
  width: var(--profile-column-gap) !important;
  flex: 0 0 var(--profile-column-gap) !important;
}

.notion-column_list-block > div > div:last-child {
  width: auto !important;
  min-width: 0 !important;
  flex: 1 1 auto !important;
}

.notion-column_list-block > div > div:first-child img {
  object-fit: contain !important;
}

.notion-column_list-block > div > div:first-child .content-editable-leaf-rtl {
  word-break: normal !important;
  overflow-wrap: anywhere !important;
}

@media (max-width: 760px) {
  :root {
    --page-inline-padding: 20px;
  }

  .layout {
    padding-bottom: 44px !important;
  }

  .notion-column_list-block > div {
    display: flex !important;
    flex-direction: column !important;
  }

  .notion-column_list-block > div > div {
    width: 100% !important;
    flex: 0 0 auto !important;
  }

  .notion-column_list-block > div > div:first-child,
  .notion-column_list-block > div > div:last-child {
    width: 100% !important;
    flex-basis: auto !important;
  }

  .notion-column_list-block > div > div:nth-child(2) {
    display: none !important;
  }

  .notion-column_list-block
    > div
    > div:first-child
    .notion-text-block:has([data-content-editable-leaf]:empty) {
    display: none !important;
  }

  .notion-column_list-block > div > div:first-child {
    padding-bottom: 8px !important;
  }

  .notion-column_list-block > div > div:last-child {
    padding-top: 8px !important;
  }
}
</style>
""".strip()


def clean_index(index_path: Path) -> None:
    html = index_path.read_text(encoding="utf-8")

    # Loconotion can serialize missing Notion assets as literal "None" URLs.
    html = re.sub(r'<link\b[^>]*\bhref=["\']None["\'][^>]*>\s*', "", html)
    html = re.sub(r'<script\b[^>]*\bsrc=["\']None["\'][^>]*>\s*</script>\s*', "", html)

    html = re.sub(
        rf'<style id=["\']{FIX_STYLE_ID}["\']>.*?</style>\s*',
        "",
        html,
        flags=re.DOTALL,
    )
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
