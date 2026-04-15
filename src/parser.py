"""
Obsidian-flavored Markdown parser.
Handles: frontmatter, wikilinks, embeds, callouts, highlights, tags.
"""
import re
from pathlib import Path

import markdown as md_lib
import yaml

CALLOUT_TYPES: dict[str, tuple[str, str]] = {
    "note":       ("ℹ",  "note"),
    "info":       ("ℹ",  "info"),
    "tip":        ("💡", "tip"),
    "hint":       ("💡", "tip"),
    "important":  ("❗", "important"),
    "warning":    ("⚠",  "warning"),
    "caution":    ("⚠",  "warning"),
    "attention":  ("⚠",  "warning"),
    "danger":     ("🔥", "danger"),
    "error":      ("🔥", "danger"),
    "success":    ("✅", "success"),
    "check":      ("✅", "success"),
    "done":       ("✅", "success"),
    "question":   ("❓", "question"),
    "help":       ("❓", "question"),
    "faq":        ("❓", "question"),
    "quote":      ("❝",  "quote"),
    "cite":       ("❝",  "quote"),
    "abstract":   ("📋", "abstract"),
    "summary":    ("📋", "abstract"),
    "tldr":       ("📋", "abstract"),
    "todo":       ("☑",  "todo"),
    "bug":        ("🐛", "bug"),
    "example":    ("📖", "example"),
    "experiment": ("🧪", "example"),
}

_MD_EXTENSIONS = [
    "fenced_code",
    "tables",
    "footnotes",
    "attr_list",
    "toc",
    "sane_lists",
    "codehilite",
]

_MD_EXTENSION_CONFIGS = {
    "codehilite": {
        "guess_lang": False,
        "use_pygments": True,
        "noclasses": False,
        "css_class": "codehilite",
    }
}


class ObsidianParser:
    """Converts a single Obsidian markdown document to HTML."""

    def __init__(self, slug_map: dict[str, str] | None = None) -> None:
        """
        slug_map: {lowercase_filename_stem: page_slug}
                  Used to resolve [[wikilinks]] to #anchor hrefs.
        """
        self.slug_map = slug_map or {}

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def parse(self, text: str) -> tuple[dict, str]:
        """Return (frontmatter_dict, html_string)."""
        frontmatter, body = self._extract_frontmatter(text)
        body = self._process_highlights(body)
        body = self._process_wikilinks(body)
        body = self._process_tags(body)
        body = self._process_callouts(body)
        html = self._convert_markdown(body)
        return frontmatter, html

    # ------------------------------------------------------------------
    # Preprocessing steps
    # ------------------------------------------------------------------

    def _extract_frontmatter(self, text: str) -> tuple[dict, str]:
        match = re.match(r"^---\s*\n(.*?)\n---\s*\n", text, re.DOTALL)
        if match:
            try:
                fm = yaml.safe_load(match.group(1)) or {}
            except Exception:
                fm = {}
            return fm, text[match.end():]
        return {}, text

    def _process_highlights(self, text: str) -> str:
        """==text== → <mark>text</mark>"""
        return re.sub(r"==([^=\n]+)==", r"<mark>\1</mark>", text)

    def _process_wikilinks(self, text: str) -> str:
        """
        ![[file]]          → <img> or embed link
        [[Page|Alias]]     → internal link with alias
        [[Page]]           → internal link
        [[Page#Heading]]   → internal link to heading
        """

        def replace_embed(m: re.Match) -> str:
            raw = m.group(1).strip()
            target, alt = (raw.split("|", 1) + [raw])[:2]
            target = target.strip()
            alt = alt.strip()
            ext = Path(target).suffix.lower()
            if ext in (".png", ".jpg", ".jpeg", ".gif", ".svg", ".webp", ".bmp", ".avif"):
                return f'<img src="{target}" alt="{alt}" class="ob-embed-img">'
            slug = self._resolve_slug(target)
            return f'<a href="#{slug}" class="internal-link ob-embed-link">📎 {alt}</a>'

        text = re.sub(r"!\[\[([^\]]+)\]\]", replace_embed, text)

        def replace_wikilink(m: re.Match) -> str:
            inner = m.group(1).strip()
            if "|" in inner:
                target, display = inner.split("|", 1)
                target = target.strip()
                display = display.strip()
            else:
                target = inner
                display = None

            heading = None
            if "#" in target:
                target, heading = target.split("#", 1)

            slug = self._resolve_slug(target) if target else ""
            href = f"#{slug}"
            if heading:
                href += f"-{self._slugify(heading)}"

            if display is None:
                display = target if target else (heading or inner)

            return f'<a href="{href}" class="internal-link">{display}</a>'

        text = re.sub(r"\[\[([^\]]+)\]\]", replace_wikilink, text)
        return text

    def _process_tags(self, text: str) -> str:
        """#tag (preceded by whitespace) → <span class="ob-tag">#tag</span>"""
        return re.sub(
            r"(?<=\s)#([a-zA-Z][a-zA-Z0-9_/:-]*)",
            r'<span class="ob-tag">#\1</span>',
            text,
        )

    def _process_callouts(self, text: str) -> str:
        """
        Convert Obsidian callout blocks to styled HTML divs.

        > [!NOTE] Optional title
        > Body content (may span multiple > lines)
        """
        lines = text.split("\n")
        result: list[str] = []
        i = 0

        while i < len(lines):
            line = lines[i]
            m = re.match(r"^> \[!(\w+)\][+\-]?\s*(.*)", line)
            if m:
                ctype = m.group(1).lower()
                title_text = m.group(2).strip()
                icon, css_class = CALLOUT_TYPES.get(ctype, ("📝", "note"))
                title = title_text if title_text else ctype.capitalize()

                # Collect continuation lines (start with ">")
                body_lines: list[str] = []
                i += 1
                while i < len(lines):
                    bl = lines[i]
                    if bl == ">":
                        body_lines.append("")
                        i += 1
                    elif bl.startswith("> "):
                        body_lines.append(bl[2:])
                        i += 1
                    elif bl.startswith(">"):
                        body_lines.append(bl[1:])
                        i += 1
                    else:
                        break

                body_md = "\n".join(body_lines)
                body_html = md_lib.markdown(
                    body_md,
                    extensions=["fenced_code", "tables", "sane_lists"],
                )

                result.append(f'<div class="ob-callout ob-callout-{css_class}">')
                result.append(f'<div class="ob-callout-title">{icon} {title}</div>')
                result.append(f'<div class="ob-callout-body">{body_html}</div>')
                result.append("</div>")
            else:
                result.append(line)
                i += 1

        return "\n".join(result)

    # ------------------------------------------------------------------
    # Markdown conversion
    # ------------------------------------------------------------------

    def _convert_markdown(self, text: str) -> str:
        processor = md_lib.Markdown(
            extensions=_MD_EXTENSIONS,
            extension_configs=_MD_EXTENSION_CONFIGS,
        )
        html = processor.convert(text)
        return self._postprocess_checkboxes(html)

    @staticmethod
    def _postprocess_checkboxes(html: str) -> str:
        """Convert GFM-style task list markers to <input type="checkbox">."""
        html = re.sub(
            r"<li>\[x\]\s*",
            '<li><input type="checkbox" checked disabled> ',
            html,
            flags=re.IGNORECASE,
        )
        html = re.sub(
            r"<li>\[ \]\s*",
            '<li><input type="checkbox" disabled> ',
            html,
        )
        return html

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    def _resolve_slug(self, name: str) -> str:
        stem = Path(name).stem
        key = stem.lower()
        return self.slug_map.get(key, self._slugify(stem))

    @staticmethod
    def _slugify(text: str) -> str:
        text = re.sub(r"[^\w\s-]", "", text.lower())
        return re.sub(r"[\s_]+", "-", text).strip("-")
