"""
HTML template generator.
Produces a single self-contained HTML file with all CSS and JS embedded.
"""
from __future__ import annotations

from pathlib import Path

from pygments.formatters import HtmlFormatter

# ---------------------------------------------------------------------------
# Pygments syntax-highlight CSS (dark: dracula, light: friendly)
# ---------------------------------------------------------------------------

def _pygments_css() -> str:
    dark = HtmlFormatter(style="dracula").get_style_defs(".codehilite")
    light = HtmlFormatter(style="friendly").get_style_defs(
        '[data-theme="light"] .codehilite'
    )
    return dark + "\n" + light


# ---------------------------------------------------------------------------
# CSS
# ---------------------------------------------------------------------------

_CSS = """
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

:root {
  --bg:           #1e1e2e;
  --sidebar-bg:   #181825;
  --text:         #cdd6f4;
  --text-muted:   #6c7086;
  --accent:       #89b4fa;
  --border:       #313244;
  --surface:      #313244;
  --mark-bg:      rgba(249,226,175,0.22);
  --mark-text:    #f9e2af;
  --link:         #89b4fa;
  --heading:      #cba6f7;
  --tag-bg:       #313244;
  --tag-text:     #89b4fa;

  --c-note:     #89b4fa;
  --c-info:     #89dceb;
  --c-tip:      #a6e3a1;
  --c-warning:  #f9e2af;
  --c-danger:   #f38ba8;
  --c-success:  #a6e3a1;
  --c-question: #cba6f7;
  --c-quote:    #9399b2;
  --c-abstract: #74c7ec;
  --c-todo:     #fab387;
  --c-bug:      #f38ba8;
  --c-example:  #cba6f7;
}

[data-theme="light"] {
  --bg:           #eff1f5;
  --sidebar-bg:   #e6e9ef;
  --text:         #4c4f69;
  --text-muted:   #8c8fa1;
  --accent:       #1e66f5;
  --border:       #ccd0da;
  --surface:      #dce0e8;
  --mark-bg:      rgba(223,142,29,0.18);
  --mark-text:    #7c5200;
  --link:         #1e66f5;
  --heading:      #8839ef;
  --tag-bg:       #dce0e8;
  --tag-text:     #1e66f5;

  --c-note:     #1e66f5;
  --c-info:     #04a5e5;
  --c-tip:      #40a02b;
  --c-warning:  #df8e1d;
  --c-danger:   #d20f39;
  --c-success:  #40a02b;
  --c-question: #8839ef;
  --c-quote:    #6c6f85;
  --c-abstract: #04a5e5;
  --c-todo:     #fe640b;
  --c-bug:      #d20f39;
  --c-example:  #8839ef;
}

html, body { height: 100%; overflow: hidden; }

body {
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto,
               "Helvetica Neue", Arial, sans-serif;
  background: var(--bg);
  color: var(--text);
  font-size: 15px;
  line-height: 1.75;
}

/* ── Layout ── */
.app { display: flex; height: 100vh; }

/* ── Sidebar ── */
.sidebar {
  width: 260px;
  flex-shrink: 0;
  background: var(--sidebar-bg);
  border-right: 1px solid var(--border);
  display: flex;
  flex-direction: column;
  overflow: hidden;
  transition: width 0.2s ease;
}
.sidebar.collapsed { width: 0; border-right: none; }

.sidebar-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 14px 16px;
  border-bottom: 1px solid var(--border);
  flex-shrink: 0;
  gap: 8px;
}
.vault-name {
  font-weight: 700;
  font-size: 13px;
  color: var(--text);
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  flex: 1;
}
.theme-btn {
  background: none;
  border: none;
  cursor: pointer;
  font-size: 15px;
  padding: 4px 6px;
  border-radius: 5px;
  color: var(--text-muted);
  flex-shrink: 0;
  line-height: 1;
}
.theme-btn:hover { background: var(--surface); color: var(--text); }

.search-wrap { padding: 10px 12px; flex-shrink: 0; }
#search {
  width: 100%;
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 6px;
  padding: 6px 10px;
  color: var(--text);
  font-size: 13px;
  outline: none;
}
#search:focus { border-color: var(--accent); }
#search::placeholder { color: var(--text-muted); }

.nav-tree { flex: 1; overflow-y: auto; padding: 6px 8px 16px; }

/* Folder */
.nav-folder { margin-bottom: 2px; }
.nav-folder-title {
  display: flex;
  align-items: center;
  gap: 5px;
  padding: 4px 8px;
  font-size: 11px;
  font-weight: 700;
  color: var(--text-muted);
  text-transform: uppercase;
  letter-spacing: 0.06em;
  cursor: pointer;
  border-radius: 5px;
  user-select: none;
}
.nav-folder-title:hover { background: var(--surface); color: var(--text); }
.folder-arrow { font-size: 9px; transition: transform 0.15s; }
.folder-arrow.open { transform: rotate(90deg); }
.nav-folder-children { padding-left: 10px; }

/* Nav items */
.nav-item { margin-bottom: 1px; }
.nav-link {
  display: block;
  padding: 5px 8px;
  border-radius: 5px;
  font-size: 13px;
  color: var(--text-muted);
  text-decoration: none;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  transition: background 0.12s, color 0.12s;
}
.nav-link:hover { background: var(--surface); color: var(--text); }
.nav-link.active { background: var(--accent); color: #fff !important; }

/* Sidebar toggle (hamburger) */
.sidebar-toggle {
  position: fixed;
  top: 10px;
  left: 10px;
  z-index: 200;
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 6px;
  padding: 5px 9px;
  cursor: pointer;
  color: var(--text);
  font-size: 15px;
  display: none;
  line-height: 1;
}

/* ── Content ── */
.content {
  flex: 1;
  overflow-y: auto;
  padding: 2.5rem 3rem;
  min-width: 0;
  transition: padding-left 0.2s;
}
.content.expanded { padding-left: 4rem; }

#pages { max-width: 760px; margin: 0 auto; }

.page { display: none; }
.page.active { display: block; }

.page-title {
  font-size: 2rem;
  font-weight: 700;
  color: var(--heading);
  margin-bottom: 1.5rem;
  padding-bottom: 0.6rem;
  border-bottom: 1px solid var(--border);
  line-height: 1.25;
}

/* ── Typography ── */
h1, h2, h3, h4, h5, h6 {
  color: var(--heading);
  margin: 1.6em 0 0.5em;
  line-height: 1.3;
}
h1 { font-size: 1.75rem; }
h2 { font-size: 1.4rem; }
h3 { font-size: 1.15rem; }
h4 { font-size: 1rem; }

p { margin: 0.7em 0; }

a { color: var(--link); text-decoration: none; }
a:hover { text-decoration: underline; }

a.internal-link { color: var(--accent); }
a.internal-link::before { content: "[["; opacity: 0.45; font-size: 0.78em; }
a.internal-link::after  { content: "]]"; opacity: 0.45; font-size: 0.78em; }

ul, ol { margin: 0.5em 0; padding-left: 1.6em; }
li { margin: 0.2em 0; }
li input[type="checkbox"] { margin-right: 6px; }

blockquote {
  border-left: 3px solid var(--border);
  margin: 1em 0;
  padding: 0.3em 1em;
  color: var(--text-muted);
}

hr { border: none; border-top: 1px solid var(--border); margin: 2em 0; }

/* ── Code ── */
code {
  background: var(--surface);
  border-radius: 4px;
  padding: 0.15em 0.4em;
  font-family: "JetBrains Mono", "Fira Code", "Cascadia Code", monospace;
  font-size: 0.86em;
}
pre {
  background: var(--surface);
  border-radius: 8px;
  padding: 1em 1.25em;
  overflow-x: auto;
  margin: 1em 0;
  border: 1px solid var(--border);
}
pre code { background: none; padding: 0; font-size: 0.875em; }

.codehilite {
  background: var(--surface) !important;
  border-radius: 8px;
  padding: 1em 1.25em;
  overflow-x: auto;
  margin: 1em 0;
  border: 1px solid var(--border);
}
.codehilite pre { background: none !important; border: none; padding: 0; margin: 0; }

/* ── Tables ── */
table { border-collapse: collapse; width: 100%; margin: 1em 0; font-size: 0.9em; }
th, td { border: 1px solid var(--border); padding: 8px 12px; text-align: left; }
th { background: var(--surface); font-weight: 600; color: var(--heading); }
tr:nth-child(even) td { background: rgba(255,255,255,0.025); }
[data-theme="light"] tr:nth-child(even) td { background: rgba(0,0,0,0.025); }

/* ── Highlights ── */
mark {
  background: var(--mark-bg);
  color: var(--mark-text);
  border-radius: 3px;
  padding: 0.05em 0.25em;
}

/* ── Tags ── */
.ob-tag {
  display: inline-block;
  background: var(--tag-bg);
  border: 1px solid var(--border);
  color: var(--tag-text);
  border-radius: 100px;
  padding: 0.05em 0.55em;
  font-size: 0.8em;
  font-weight: 500;
  text-decoration: none;
}

/* ── Images ── */
img, .ob-embed-img { max-width: 100%; border-radius: 6px; margin: 0.5em 0; }

/* ── Callouts ── */
.ob-callout {
  border-radius: 6px;
  margin: 1.2em 0;
  border: 1px solid;
  border-left-width: 4px;
  overflow: hidden;
}

.ob-callout-note     { --cc: var(--c-note);     }
.ob-callout-info     { --cc: var(--c-info);     }
.ob-callout-tip      { --cc: var(--c-tip);      }
.ob-callout-warning  { --cc: var(--c-warning);  }
.ob-callout-danger   { --cc: var(--c-danger);   }
.ob-callout-success  { --cc: var(--c-success);  }
.ob-callout-question { --cc: var(--c-question); }
.ob-callout-quote    { --cc: var(--c-quote);    }
.ob-callout-abstract { --cc: var(--c-abstract); }
.ob-callout-todo     { --cc: var(--c-todo);     }
.ob-callout-bug      { --cc: var(--c-bug);      }
.ob-callout-example  { --cc: var(--c-example);  }

.ob-callout {
  border-color: var(--cc, var(--border));
}
.ob-callout-title {
  padding: 8px 14px;
  font-weight: 600;
  font-size: 0.88em;
  color: var(--cc, var(--text));
  background: color-mix(in srgb, var(--cc, var(--border)) 12%, transparent);
}
.ob-callout-body {
  padding: 10px 14px;
  font-size: 0.95em;
  background: color-mix(in srgb, var(--cc, var(--border)) 5%, var(--bg));
}
.ob-callout-body > *:first-child { margin-top: 0; }
.ob-callout-body > *:last-child  { margin-bottom: 0; }

/* ── Footnotes ── */
.footnote { font-size: 0.85em; color: var(--text-muted); margin-top: 2em; border-top: 1px solid var(--border); padding-top: 1em; }

/* ── Responsive ── */
@media (max-width: 768px) {
  .sidebar {
    position: fixed;
    top: 0; left: 0; bottom: 0;
    z-index: 100;
    transition: transform 0.2s ease;
  }
  .sidebar.collapsed { width: 260px; transform: translateX(-260px); }
  .sidebar-toggle { display: block; }
  .content { padding: 3.5rem 1.25rem 1.5rem; }
  .content.expanded { padding-left: 1.25rem; }
}

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 5px; height: 5px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: var(--border); border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: var(--text-muted); }
"""

# ---------------------------------------------------------------------------
# JavaScript
# ---------------------------------------------------------------------------

_JS = """
(function () {
  'use strict';

  // Restore theme before first paint
  var saved = localStorage.getItem('ob-theme') || 'dark';
  document.documentElement.setAttribute('data-theme', saved);
  updateThemeBtn(saved);

  document.addEventListener('DOMContentLoaded', function () {
    navigate();
    // Open all folders by default
    document.querySelectorAll('.nav-folder-children').forEach(function (el) {
      el.style.display = '';
    });
    document.querySelectorAll('.folder-arrow').forEach(function (el) {
      el.classList.add('open');
    });
  });

  window.addEventListener('hashchange', navigate);

  window.navigate = function () {
    var hash = decodeURIComponent(location.hash.slice(1));
    showPage(hash || FIRST_SLUG);
  };

  window.showPage = function (slug) {
    document.querySelectorAll('.page').forEach(function (p) {
      p.classList.remove('active');
    });
    var page = document.getElementById(slug);
    if (page) {
      page.classList.add('active');
      document.querySelectorAll('.nav-link').forEach(function (a) {
        var href = decodeURIComponent((a.getAttribute('href') || '').slice(1));
        a.classList.toggle('active', href === slug);
      });
      var vaultName = document.querySelector('.vault-name').textContent;
      document.title = (page.dataset.title || slug) + ' \u2013 ' + vaultName;
      var content = document.getElementById('content');
      if (content) content.scrollTop = 0;
    } else if (FIRST_SLUG) {
      showPage(FIRST_SLUG);
    }
  };

  window.toggleTheme = function () {
    var current = document.documentElement.getAttribute('data-theme');
    var next = current === 'dark' ? 'light' : 'dark';
    document.documentElement.setAttribute('data-theme', next);
    localStorage.setItem('ob-theme', next);
    updateThemeBtn(next);
  };

  function updateThemeBtn(theme) {
    var btn = document.querySelector('.theme-btn');
    if (btn) btn.textContent = theme === 'dark' ? '\u2600' : '\U0001F319';
  }

  window.filterPages = function (query) {
    var q = query.toLowerCase().trim();
    document.querySelectorAll('.nav-item').forEach(function (item) {
      var link = item.querySelector('.nav-link');
      var match = !q || link.textContent.toLowerCase().includes(q);
      item.style.display = match ? '' : 'none';
    });
    document.querySelectorAll('.nav-folder').forEach(function (folder) {
      if (!q) { folder.style.display = ''; return; }
      var hasVisible = Array.from(folder.querySelectorAll('.nav-item'))
        .some(function (i) { return i.style.display !== 'none'; });
      folder.style.display = hasVisible ? '' : 'none';
    });
  };

  window.toggleSidebar = function () {
    document.getElementById('sidebar').classList.toggle('collapsed');
    document.getElementById('content').classList.toggle('expanded');
  };

  window.toggleFolder = function (el) {
    var children = el.nextElementSibling;
    if (children) {
      children.style.display = children.style.display === 'none' ? '' : 'none';
    }
    var arrow = el.querySelector('.folder-arrow');
    if (arrow) arrow.classList.toggle('open');
  };
}());
"""

# ---------------------------------------------------------------------------
# Navigation tree builder
# ---------------------------------------------------------------------------


def _build_tree(pages: list[dict]) -> dict:
    """Nest pages into a folder tree dict.

    Returns: {'_pages': [...], 'folder_name': {'_pages': [...], ...}}
    """
    tree: dict = {"_pages": []}
    for page in pages:
        parts = page["folder"].split("/") if page["folder"] else []
        node = tree
        for part in parts:
            if part not in node:
                node[part] = {"_pages": []}
            node = node[part]
        node["_pages"].append(page)
    return tree


def _render_tree(node: dict, depth: int = 0) -> str:
    html = ""
    # Files at this level
    for page in sorted(node["_pages"], key=lambda p: p["title"].lower()):
        slug = page["slug"]
        title = page["title"]
        html += f'<div class="nav-item"><a href="#{slug}" class="nav-link" title="{title}">📄 {title}</a></div>\n'
    # Sub-folders
    for key in sorted(k for k in node if k != "_pages"):
        html += '<div class="nav-folder">\n'
        html += (
            f'<div class="nav-folder-title" onclick="toggleFolder(this)">'
            f'<span class="folder-arrow">▶</span> 📁 {key}'
            f"</div>\n"
        )
        html += '<div class="nav-folder-children">\n'
        html += _render_tree(node[key], depth + 1)
        html += "</div>\n</div>\n"
    return html


def _build_nav(pages: list[dict]) -> str:
    tree = _build_tree(pages)
    return _render_tree(tree)


# ---------------------------------------------------------------------------
# Public entry point
# ---------------------------------------------------------------------------


def generate_html(pages: list[dict], title: str = "My Vault") -> str:
    """
    pages: list of {slug, title, html, folder, frontmatter, path}
    Returns a complete, self-contained HTML string.
    """
    if not pages:
        raise ValueError("No pages to render")

    first_slug = pages[0]["slug"]
    nav_html = _build_nav(pages)
    pygments_css = _pygments_css()

    pages_html_parts = []
    for page in pages:
        slug = page["slug"]
        ptitle = page["title"].replace('"', "&quot;")
        pages_html_parts.append(
            f'<div class="page" id="{slug}" data-title="{ptitle}">\n'
            f'<h1 class="page-title">{page["title"]}</h1>\n'
            f'{page["html"]}\n'
            f"</div>"
        )
    pages_html = "\n".join(pages_html_parts)

    # Escape title for HTML attribute / JS string
    title_safe = title.replace('"', "&quot;").replace("<", "&lt;").replace(">", "&gt;")

    return f"""<!DOCTYPE html>
<html lang="en" data-theme="dark">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title_safe}</title>
  <style>
{_CSS}
{pygments_css}
  </style>
</head>
<body>
  <div class="app">
    <nav class="sidebar" id="sidebar">
      <div class="sidebar-header">
        <span class="vault-name">{title_safe}</span>
        <button class="theme-btn" onclick="toggleTheme()" title="Toggle theme">&#9728;</button>
      </div>
      <div class="search-wrap">
        <input type="text" id="search" placeholder="&#128269; Search pages…"
               oninput="filterPages(this.value)" autocomplete="off">
      </div>
      <div class="nav-tree" id="nav-tree">
        {nav_html}
      </div>
    </nav>

    <button class="sidebar-toggle" id="sidebar-toggle"
            onclick="toggleSidebar()" title="Toggle sidebar">&#9776;</button>

    <main class="content" id="content">
      <div id="pages">
{pages_html}
      </div>
    </main>
  </div>

  <script>
    var FIRST_SLUG = {first_slug!r};
{_JS}
  </script>
</body>
</html>"""
