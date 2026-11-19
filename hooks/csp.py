"""Make the built pages work under the site's Content-Security-Policy, which has no
'unsafe-inline' in script-src.

docs.witfoo.com is served with the CSP in content-security-policy.txt (set at the CDN;
that file is the copy to paste there). The Material theme writes small scripts inline
into every page, and one <style> element. This hook rewrites each built page:

* An inline script whose SHA-256 is listed in script-src stays inline: the browser
  allows it by its hash. Only the theme's two content scripts are listed (restore the
  reader's linked content tab; open the tab named by the URL hash). They are the same
  on every page, so their hashes change only when a Material release changes them.
* Every other executable inline script is moved into a file under
  assets/javascripts/inline/ named by the hash of its content, and a <script src> takes
  its place. A <script src> without async or defer runs where it stands, as the inline
  one did. These are the theme's head and header scripts (localStorage scope, which
  differs with page depth, and the saved colour palette).
* Each inline <style> element is moved the same way into assets/stylesheets/inline/.
* The theme's no-op href="javascript:void(0)" on the search share link becomes "#".
  The theme replaces that href and cancels every click on the link, so it never ran.

Why the content scripts are not moved as well: they sit inside the part of the page
that instant navigation swaps. The theme re-runs the scripts it swaps in, and waits for
each <script src> to load before it tells the rest of the theme that the new page is
there. In that gap the previous page's table-of-contents tracking is still live and can
write one of the previous page's headings into the new page's URL. Inline scripts run
in the same step as the swap, so there is no gap.

Warnings fail `mkdocs build --strict` (the PR check). The hook warns when:

* it had to move a script from inside that swapped part of the page (after a Material
  upgrade, this is a content script whose hash changed: add the new 'sha256-...' to
  script-src in content-security-policy.txt, add it to the CDN rule BEFORE merging,
  and remove the old one after the release is live). The page still works meanwhile:
  the moved script runs from its file;
* a page has an on* event-handler attribute (onclick=...) or a javascript: URL, which
  script-src blocks. Put behaviour in a .js file under docs/assets/ and list it in
  extra_javascript instead.

style-src keeps 'unsafe-inline': the Mermaid diagrams draw with <style> elements and
style="" attributes created at run time, which no build step can move. style="" in the
Markdown is therefore not reported.
"""

from __future__ import annotations

import base64
import hashlib
import logging
import os
import posixpath
import re

log = logging.getLogger("mkdocs.hooks.csp")

POLICY_FILE = "content-security-policy.txt"

# Script types the browser executes. Anything else (application/json, the theme's
# __config block) is data: CSP does not block it and the theme reads it as text.
_EXECUTABLE = {"", "text/javascript", "application/javascript", "module",
               "text/ecmascript", "application/ecmascript"}

_SCRIPT = re.compile(r"<script(?P<attrs>(?:\s[^>]*)?)>(?P<body>.*?)</script\s*>", re.S | re.I)
_STYLE = re.compile(r"<style(?P<attrs>(?:\s[^>]*)?)>(?P<body>.*?)</style\s*>", re.S | re.I)
_ATTR = re.compile(r"""([^\s=/>]+)(?:\s*=\s*(?:"([^"]*)"|'([^']*)'|([^\s>]+)))?""")
# Only the theme's search share link (data-md-component=search-share): an author's
# javascript: URL must reach the guard below, not be rewritten silently.
_NOOP_JS_HREF = re.compile(r"""(<a\b(?=[^>]*\bdata-md-component=["']?search-share\b)[^>]*?\bhref\s*=\s*)(["']?)javascript:\s*void\(0\);?\2(?=[\s>])""", re.I)
_PRE = re.compile(r"<(pre|code|textarea)\b.*?</\1\s*>", re.S | re.I)
_TAG = re.compile(r"<[a-zA-Z][^\s/>]*(?P<attrs>(?:\s[^>]*)?)>")
_URL_ATTRS = {"href", "src", "action", "formaction", "xlink:href"}
# The part of the page instant navigation swaps, and the first element after it.
_SWAP_START = re.compile(r"""data-md-component=["']?container\b""")
_SWAP_END = re.compile(r"""data-md-component=["']?dialog\b|</body""", re.I)

_SCRIPT_DIR = "assets/javascripts/inline"
_STYLE_DIR = "assets/stylesheets/inline"

_base_urls: dict[str, str] = {}
_allowed: set[str] = set()
_warned: set[str] = set()


def _attrs(raw: str) -> dict[str, str]:
    out = {}
    for m in _ATTR.finditer(raw or ""):
        out[m.group(1).lower()] = next((g for g in m.group(2, 3, 4) if g is not None), "")
    return out


def _sha256(body: str) -> str:
    return "sha256-" + base64.b64encode(hashlib.sha256(body.encode("utf-8")).digest()).decode()


def _write(site_dir: str, folder: str, body: str, ext: str) -> str:
    data = body.encode("utf-8")
    name = f"{hashlib.sha256(data).hexdigest()[:16]}.{ext}"
    path = os.path.join(site_dir, folder, name)
    if not os.path.exists(path):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "wb") as fh:
            fh.write(data)
    return f"{folder}/{name}"


def _url(base_url: str, path: str) -> str:
    # The same base the theme's own asset links use ('.', '../..', or '/' on 404.html).
    if not base_url:
        return path
    return posixpath.join(base_url, path)


def on_config(config):
    path = os.path.join(os.path.dirname(config.config_file_path), POLICY_FILE)
    with open(path, encoding="utf-8") as fh:
        policy = fh.read()
    _allowed.clear()
    _warned.clear()
    for directive in policy.split(";"):
        parts = directive.split()
        if parts and parts[0].lower() == "script-src":
            _allowed.update(p.strip("'") for p in parts[1:] if p.startswith("'sha256-"))
    return config


def on_page_context(context, page, config, nav):
    _base_urls[page.file.src_uri] = context.get("base_url", "")
    return context


def on_template_context(context, template_name, config):
    # Theme templates rendered outside a page: 404.html (and sitemap.xml, left alone).
    _base_urls["template:" + template_name] = context.get("base_url", "")
    return context


def on_post_page(output, page, config):
    return _rewrite(output, config["site_dir"], _base_urls.pop(page.file.src_uri, ""),
                    page.file.src_uri)


def on_post_template(output, template_name, config):
    base_url = _base_urls.pop("template:" + template_name, "")
    if not template_name.endswith(".html"):
        return output
    return _rewrite(output, config["site_dir"], base_url, template_name)


def _rewrite(output, site_dir, base_url, label):
    start = _SWAP_START.search(output)
    end = _SWAP_END.search(output, start.end()) if start else None
    swapped = (start.start(), end.start() if end else len(output)) if start else (0, 0)
    moved_from_swap = []

    def script(m):
        attrs = _attrs(m.group("attrs"))
        kind = attrs.get("type", "").strip().lower()
        body = m.group("body")
        if "src" in attrs or kind not in _EXECUTABLE or not body.strip():
            return m.group(0)
        digest = _sha256(body)
        if digest in _allowed:
            return m.group(0)
        if swapped[0] <= m.start() < swapped[1]:
            moved_from_swap.append(digest)
        rel = _write(site_dir, _SCRIPT_DIR, body, "js")
        type_attr = ' type="module"' if kind == "module" else ""
        return f'<script src="{_url(base_url, rel)}"{type_attr}></script>'

    def style(m):
        body = m.group("body")
        if not body.strip():
            return ""
        media = _attrs(m.group("attrs")).get("media")
        rel = _write(site_dir, _STYLE_DIR, body, "css")
        media_attr = f' media="{media}"' if media else ""
        return f'<link rel="stylesheet" href="{_url(base_url, rel)}"{media_attr}>'

    output = _SCRIPT.sub(script, output)
    # Move only the theme's <head> styles: in an inline <svg> a <link> is foreign content
    # and loads nothing, so a moved diagram <style> would silently drop its styling.
    head_end = output.find("</head>")
    if head_end != -1:
        output = _STYLE.sub(style, output[:head_end]) + output[head_end:]
    output = _NOOP_JS_HREF.sub(r'\1"#"', output)

    for digest in moved_from_swap:
        if digest in _warned:
            continue
        _warned.add(digest)
        log.warning("%s: moved an inline script out of the instant-navigation container "
                    "('%s' is not in script-src in %s); see hooks/csp.py", label, digest,
                    POLICY_FILE)

    # Report what script-src blocks and cannot be moved. Code samples are escaped text,
    # not markup, but skip them anyway so a sample that shows a tag is never counted.
    markup = _PRE.sub("", output)
    found = {"on* event-handler attribute": 0, "javascript: URL": 0}
    for tag in _TAG.finditer(markup):
        attrs = _attrs(tag.group("attrs"))
        found["on* event-handler attribute"] += any(k.startswith("on") for k in attrs)
        found["javascript: URL"] += any(
            k in _URL_ATTRS and v.strip().lower().startswith("javascript:") for k, v in attrs.items())
    for what, n in found.items():
        if n:
            log.warning("%s: %d element(s) with an inline %s, which the site's CSP blocks; "
                        "see hooks/csp.py", label, n, what)
    return output
