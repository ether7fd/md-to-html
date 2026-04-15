#!/usr/bin/env python3
"""
Obsidian Vault → Single HTML Converter
Usage:
    python convert.py <vault_folder> [-o output.html] [--title "My Notes"]
"""
import argparse
import re
import sys
from pathlib import Path

from src.parser import ObsidianParser
from src.template import generate_html


def slugify(text: str) -> str:
    """Convert a relative path (without ext) to a URL-safe slug."""
    text = text.replace("\\", "/").replace("/", "-")
    text = re.sub(r"[^\w-]", "-", text.lower())
    return re.sub(r"-+", "-", text).strip("-")


def main() -> None:
    ap = argparse.ArgumentParser(
        description="Convert an Obsidian vault folder to a single self-contained HTML file."
    )
    ap.add_argument("input", help="Vault folder containing .md files")
    ap.add_argument("-o", "--output", default="output.html", help="Output HTML file (default: output.html)")
    ap.add_argument("--title", default="", help="Vault title shown in the sidebar (default: folder name)")
    args = ap.parse_args()

    input_path = Path(args.input).expanduser().resolve()
    if not input_path.is_dir():
        print(f"Error: '{input_path}' is not a directory.", file=sys.stderr)
        sys.exit(1)

    md_files = sorted(input_path.rglob("*.md"))
    if not md_files:
        print(f"No .md files found in '{input_path}'.", file=sys.stderr)
        sys.exit(1)

    vault_title = args.title or input_path.name

    # ── Build slug map: lowercase stem → full slug ──────────────────────────
    # In Obsidian, [[Note]] resolves by filename regardless of folder.
    # We map each stem to the first matching slug (alphabetical order).
    slug_map: dict[str, str] = {}
    for f in md_files:
        rel = f.relative_to(input_path).with_suffix("")
        slug = slugify(str(rel))
        stem = f.stem.lower()
        if stem not in slug_map:          # first occurrence wins
            slug_map[stem] = slug

    # ── Parse all files ──────────────────────────────────────────────────────
    parser = ObsidianParser(slug_map=slug_map)
    pages: list[dict] = []

    for md_file in md_files:
        try:
            text = md_file.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            text = md_file.read_text(encoding="latin-1")

        frontmatter, html = parser.parse(text)

        rel = md_file.relative_to(input_path)
        rel_no_ext = rel.with_suffix("")
        slug = slugify(str(rel_no_ext))

        # Title: frontmatter > filename
        title = (
            frontmatter.get("title")
            or frontmatter.get("name")
            or md_file.stem.replace("-", " ").replace("_", " ")
        )

        folder = str(rel_no_ext.parent) if str(rel_no_ext.parent) != "." else ""

        pages.append(
            {
                "slug": slug,
                "title": str(title),
                "html": html,
                "folder": folder,
                "frontmatter": frontmatter,
                "path": str(rel),
            }
        )

    # ── Generate & write HTML ────────────────────────────────────────────────
    output_html = generate_html(pages, title=vault_title)

    output_path = Path(args.output).expanduser().resolve()
    output_path.write_text(output_html, encoding="utf-8")

    kb = len(output_html.encode()) / 1024
    print(f"✓ {len(pages)} pages → {output_path}  ({kb:.1f} KB)")


if __name__ == "__main__":
    main()
