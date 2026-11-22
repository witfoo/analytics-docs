"""Serve the Mermaid diagrams as pre-rendered markup, so no page needs inline style.

Without this hook the theme loads mermaid.min.js on a page that has a diagram, and
Mermaid draws the diagram in the reader's browser. Mermaid styles what it draws with a
<style> element and hundreds of style="" attributes, written at run time, and the theme
copies that markup into a shadow root. The site's CSP has no 'unsafe-inline' in
style-src, so the browser blocks all of it and the diagrams render broken.

Instead, each diagram is rendered ahead of time by scripts/render-diagrams.sh, which
runs the theme's own Mermaid integration in a headless Chromium and saves the markup the
theme put in the shadow root, as diagrams/svg/<key>.html. The key is a hash of the
diagram's source text, the renderer pins (Mermaid, Playwright and Chromium, in
diagrams/renderer.json) and the theme pin (requirements.txt), so editing a diagram or
bumping any pin makes the committed render stale on its own. This hook then replaces each
<pre class="mermaid"> with:

    <div class="mermaid mermaid-static"><template>
      <link rel="stylesheet" href=".../assets/stylesheets/mermaid/<hash>.css">
      <svg ... data-mmd-style="..."> ... </svg>
    </template></div>

* The diagram's <style> element goes to a file under assets/stylesheets/mermaid/,
  loaded by the <link>.
* Each style="..." attribute becomes data-mmd-style="...".
  docs/assets/javascripts/mermaid-static.js attaches a closed shadow root to the div,
  as the theme does, copies the template into it and applies each data-mmd-style value
  through the CSSOM (element.style.cssText). CSP does not govern CSSOM writes, and an
  element.style value has exactly the precedence of the attribute it replaces.
* The div keeps the class "mermaid", so the theme's .mermaid rule (margin and
  line-height) still applies. The theme only renders pre.mermaid, so it leaves the div
  alone and never loads mermaid.min.js.

Warnings fail `mkdocs build --strict` (the PR check). The hook warns when a diagram has
no committed render (run scripts/render-diagrams.sh) and when diagrams/svg/ holds a
render no page uses. A diagram without a render is left as it was: the theme renders it
in the browser, which works only under a style-src with 'unsafe-inline'.

DOCS_MERMAID_CAPTURE=1 (set by scripts/render-diagrams.sh) leaves every diagram to the
theme and marks each <pre class="mermaid"> with data-diagram-key="<key>", so the render
script knows which file each diagram belongs in.
"""

from __future__ import annotations

import hashlib
import html
import json
import logging
import os
import posixpath
import re

log = logging.getLogger("mkdocs.hooks.mermaid_static")

RENDER_DIR = "diagrams/svg"
RENDERER_FILE = "diagrams/renderer.json"
REQUIREMENTS_FILE = "requirements.txt"
CSS_DIR = "assets/stylesheets/mermaid"
CAPTURE_ENV = "DOCS_MERMAID_CAPTURE"

# pymdownx.superfences' fence_code_format output, quoted or (after the minify plugin)
# unquoted: <pre class="mermaid"><code>escaped source</code></pre>.
_PRE = re.compile(r"""<pre\s+class=(["']?)mermaid\1\s*><code>(?P<src>.*?)</code></pre>""", re.S)
# A start tag as the browser serialises it: every attribute value in double quotes.
_START_TAG = re.compile(r"""<[A-Za-z][^\s/>]*(?:\s+[^\s"'=/>]+(?:="[^"]*")?)*\s*/?>""")
_STYLE_ATTR = re.compile(r"""(\s)style(=")""")
_STYLE_EL = re.compile(r"<style\b[^>]*>(?P<css>.*?)</style\s*>", re.S | re.I)

_state: dict = {}


def _salt(root: str) -> str:
    # Every pin that can change a render: each entry of diagrams/renderer.json (Mermaid,
    # its sha256, Playwright and the Chromium it drives) and the theme's pin.
    with open(os.path.join(root, RENDERER_FILE), encoding="utf-8") as fh:
        renderer = json.load(fh)
    material = "unpinned"
    with open(os.path.join(root, REQUIREMENTS_FILE), encoding="utf-8") as fh:
        for line in fh:
            m = re.match(r"\s*mkdocs-material\s*==\s*(\S+)", line)
            if m:
                material = m.group(1)
    pins = "".join(f"{k} {renderer[k]}\n" for k in sorted(renderer))
    return f"{pins}mkdocs-material {material}\n"


def diagram_key(salt: str, source: str) -> str:
    return hashlib.sha256((salt + source).encode("utf-8")).hexdigest()[:20]


def on_config(config):
    root = os.path.dirname(config.config_file_path)
    _state.clear()
    _state.update(
        root=root,
        salt=_salt(root),
        capture=os.environ.get(CAPTURE_ENV) == "1",
        used=set(),
        base_urls={},
    )
    return config


def on_page_context(context, page, config, nav):
    _state["base_urls"][page.file.src_uri] = context.get("base_url", "")
    return context


def _static(svg: str, site_dir: str, base_url: str, label: str) -> str:
    css = "\n".join(html.unescape(m.group("css")) for m in _STYLE_EL.finditer(svg))
    svg = _STYLE_EL.sub("", svg)
    svg = _START_TAG.sub(lambda t: _STYLE_ATTR.sub(r"\1data-mmd-style\2", t.group(0)), svg)
    if re.search(r"<style\b|\sstyle=", svg, re.I):
        log.warning("%s: a pre-rendered diagram still carries inline style; see "
                    "hooks/mermaid_static.py", label)
    data = css.encode("utf-8")
    name = f"{hashlib.sha256(data).hexdigest()[:16]}.css"
    path = os.path.join(site_dir, CSS_DIR, name)
    if not os.path.exists(path):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "wb") as fh:
            fh.write(data)
    href = posixpath.join(base_url, CSS_DIR, name) if base_url else f"{CSS_DIR}/{name}"
    return (f'<div class="mermaid mermaid-static"><template>'
            f'<link rel="stylesheet" href="{href}">{svg}</template></div>')


def on_post_page(output, page, config):
    label = page.file.src_uri
    base_url = _state["base_urls"].pop(label, "")
    missing = []

    def replace(m):
        key = diagram_key(_state["salt"], html.unescape(m.group("src")))
        render = os.path.join(_state["root"], RENDER_DIR, key + ".html")
        if _state["capture"] or not os.path.exists(render):
            if not _state["capture"]:
                missing.append(key)
            return m.group(0).replace("<pre ", f'<pre data-diagram-key="{key}" ', 1)
        _state["used"].add(key)
        with open(render, encoding="utf-8") as fh:
            return _static(fh.read().strip(), config["site_dir"], base_url, label)

    output = _PRE.sub(replace, output)
    for key in missing:
        log.warning("%s: Mermaid diagram %s has no render in %s/ (it is new, edited, or a "
                    "pin in %s or %s changed); run scripts/render-diagrams.sh", label, key,
                    RENDER_DIR, RENDERER_FILE, REQUIREMENTS_FILE)
    return output


def on_post_build(config):
    if _state["capture"]:
        return
    folder = os.path.join(_state["root"], RENDER_DIR)
    present = {f[:-5] for f in os.listdir(folder) if f.endswith(".html")} if os.path.isdir(folder) else set()
    for key in sorted(present - _state["used"]):
        log.warning("%s/%s.html is not used by any page; run scripts/render-diagrams.sh, "
                    "which removes stale renders", RENDER_DIR, key)
