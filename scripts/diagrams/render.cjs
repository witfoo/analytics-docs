// Pre-renders the site's Mermaid diagrams for hooks/mermaid_static.py.
// Run it through scripts/render-diagrams.sh, which builds the site in capture mode first.
//
// usage: node render.cjs SITE_DIR RENDER_DIR RENDERER_JSON SITE_URL
//
// SITE_DIR is a build made with DOCS_MERMAID_CAPTURE=1, where each <pre class="mermaid">
// carries data-diagram-key. Every page with a diagram is opened in headless Chromium and
// the theme renders the diagrams exactly as it does for a reader (its own Mermaid config,
// themeCSS and fonts). The markup the theme puts in each diagram's shadow root is saved
// as RENDER_DIR/<key>.html, and renders no page uses any more are removed.
//
// Nothing leaves the machine: every request to SITE_URL is answered from SITE_DIR and any
// other request is aborted. The theme's mermaid.min.js is the copy the privacy plugin put
// in SITE_DIR, and it must match the sha256 pinned in RENDERER_JSON. When the theme's
// floating mermaid@11 has moved past the pin, either bump the pin (and re-render every
// diagram) or pass the pinned file as MERMAID_JS=path; MERMAID_FETCH=1 downloads the pinned
// version from unpkg instead. Playwright and its Chromium must be the versions pinned in
// RENDERER_JSON too: Chromium measures the label text, so another version can move a box.
"use strict";
const fs = require("fs");
const path = require("path");
const crypto = require("crypto");
const PLAYWRIGHT = process.env.PLAYWRIGHT_MODULE || "playwright";
const { chromium } = require(PLAYWRIGHT);
const playwrightVersion = require(path.join(path.dirname(require.resolve(PLAYWRIGHT)), "package.json")).version;

const [SITE_DIR, RENDER_DIR, RENDERER_JSON, SITE_URL] = process.argv.slice(2);
if (!SITE_URL) {
  console.error("usage: node render.cjs SITE_DIR RENDER_DIR RENDERER_JSON SITE_URL");
  process.exit(2);
}
const origin = new URL(SITE_URL).origin;
const renderer = JSON.parse(fs.readFileSync(RENDERER_JSON, "utf8"));
const TYPES = { ".html": "text/html; charset=utf-8", ".js": "text/javascript", ".css": "text/css",
  ".json": "application/json", ".svg": "image/svg+xml", ".png": "image/png", ".ico": "image/x-icon",
  ".woff2": "font/woff2", ".woff": "font/woff", ".ttf": "font/ttf", ".xml": "application/xml" };
const MERMAID_PATH = /^\/assets\/external\/unpkg\.com\/mermaid@[^/]+\/dist\/mermaid\.min\.js$/;

function builtMermaid() {
  // The privacy plugin's copy, at assets/external/unpkg.com/mermaid@<range>/dist/.
  const dir = path.join(SITE_DIR, "assets", "external", "unpkg.com");
  const found = fs.existsSync(dir) ? fs.readdirSync(dir).filter((d) => d.startsWith("mermaid@"))
    .map((d) => path.join(dir, d, "dist", "mermaid.min.js")).filter((f) => fs.existsSync(f)) : [];
  if (found.length !== 1) throw new Error(`expected one mermaid.min.js under ${dir}, found ${found.length}`);
  return found[0];
}

async function pinnedMermaid() {
  let body, from;
  if (process.env.MERMAID_JS) {
    from = process.env.MERMAID_JS;
    body = fs.readFileSync(from);
  } else if (process.env.MERMAID_FETCH === "1") {
    from = `https://unpkg.com/mermaid@${renderer.mermaid}/dist/mermaid.min.js`;
    const res = await fetch(from);
    if (!res.ok) throw new Error(`${from}: HTTP ${res.status}`);
    body = Buffer.from(await res.arrayBuffer());
  } else {
    from = builtMermaid();
    body = fs.readFileSync(from);
  }
  const sum = crypto.createHash("sha256").update(body).digest("hex");
  if (sum !== renderer.mermaid_sha256) {
    throw new Error(`${from}: sha256 ${sum} is not the pinned ${renderer.mermaid_sha256} (mermaid ` +
      `${renderer.mermaid}). Bump the pin in diagrams/renderer.json and re-render, or pass the ` +
      `pinned file as MERMAID_JS=path (MERMAID_FETCH=1 downloads it)`);
  }
  return body;
}

function pagesWithDiagrams() {
  const out = [];
  (function walk(dir) {
    for (const ent of fs.readdirSync(dir, { withFileTypes: true })) {
      const p = path.join(dir, ent.name);
      if (ent.isDirectory()) walk(p);
      else if (ent.name.endsWith(".html")) {
        const keys = [...fs.readFileSync(p, "utf8").matchAll(/<pre data-diagram-key="([0-9a-f]+)"/g)].map((m) => m[1]);
        if (keys.length) out.push({ file: p, keys });
      }
    }
  })(SITE_DIR);
  return out.sort((a, b) => a.file.localeCompare(b.file));
}

function urlFor(file) {
  const rel = path.relative(SITE_DIR, file).split(path.sep).join("/");
  return `${origin}/${rel.replace(/(^|\/)index\.html$/, "$1")}`;
}

(async () => {
  const mermaidJs = await pinnedMermaid();
  const pages = pagesWithDiagrams();
  if (!pages.length) throw new Error(`no data-diagram-key in ${SITE_DIR}: build it with DOCS_MERMAID_CAPTURE=1`);
  const root = path.resolve(SITE_DIR);

  if (playwrightVersion !== renderer.playwright) {
    throw new Error(`Playwright ${playwrightVersion} is not the pinned ${renderer.playwright} (diagrams/renderer.json)`);
  }
  const browser = await chromium.launch();
  if (browser.version() !== renderer.chromium) {
    await browser.close();
    throw new Error(`Chromium ${browser.version()} is not the pinned ${renderer.chromium} (diagrams/renderer.json)`);
  }
  const context = await browser.newContext({ viewport: { width: 1280, height: 900 } });
  let page;
  await context.route("**/*", async (route) => {
    const url = new URL(route.request().url());
    if (url.origin !== origin) return route.abort();
    if (MERMAID_PATH.test(url.pathname)) {
      // Measure labels with the site's own font, never a fallback that is still loading.
      await page.evaluate(() => Promise.all(['400 1em "IBM Plex Sans"', '700 1em "IBM Plex Sans"',
        '400 1em "IBM Plex Mono"'].map((f) => document.fonts.load(f))));
      return route.fulfill({ status: 200, contentType: TYPES[".js"], body: mermaidJs });
    }
    let file = path.resolve(root, "." + decodeURIComponent(url.pathname));
    if (url.pathname.endsWith("/")) file = path.join(file, "index.html");
    if (!file.startsWith(root + path.sep) || !fs.existsSync(file) || !fs.statSync(file).isFile()) {
      return route.fulfill({ status: 404, body: "" });
    }
    return route.fulfill({ status: 200, contentType: TYPES[path.extname(file)] || "application/octet-stream",
      body: fs.readFileSync(file) });
  });
  // The theme mounts each diagram in a closed shadow root; open it so it can be read.
  await context.addInitScript(() => {
    const attach = Element.prototype.attachShadow;
    Element.prototype.attachShadow = function (init) { return attach.call(this, { ...init, mode: "open" }); };
  });
  page = await context.newPage();

  const renders = new Map();
  for (const { file, keys } of pages) {
    const url = urlFor(file);
    await page.goto(url, { waitUntil: "load" });
    await page.waitForFunction((n) => {
      const hosts = document.querySelectorAll("article pre.mermaid, article div.mermaid");
      return hosts.length === n && [...hosts].every((d) => d.tagName === "DIV" && d.shadowRoot && d.shadowRoot.innerHTML);
    }, keys.length, { timeout: 60000 });
    const svgs = await page.evaluate(() => [...document.querySelectorAll("article div.mermaid")].map((d) => d.shadowRoot.innerHTML));
    if (svgs.length !== keys.length) throw new Error(`${url}: ${keys.length} diagrams in the HTML, ${svgs.length} rendered`);
    keys.forEach((key, i) => { if (!renders.has(key)) renders.set(key, svgs[i]); });
    console.log(`${url}: ${keys.length} diagram(s)`);
  }
  await browser.close();

  fs.mkdirSync(RENDER_DIR, { recursive: true });
  let written = 0, unchanged = 0, removed = 0;
  for (const [key, svg] of renders) {
    const out = path.join(RENDER_DIR, `${key}.html`);
    const body = svg + "\n";
    if (fs.existsSync(out) && fs.readFileSync(out, "utf8") === body) { unchanged++; continue; }
    fs.writeFileSync(out, body);
    written++;
  }
  for (const name of fs.readdirSync(RENDER_DIR)) {
    if (name.endsWith(".html") && !renders.has(name.slice(0, -5))) {
      fs.unlinkSync(path.join(RENDER_DIR, name));
      removed++;
    }
  }
  console.log(`${renders.size} diagram(s) on ${pages.length} page(s): ${written} written, ${unchanged} unchanged, ${removed} removed`);
})().catch((err) => { console.error(err); process.exit(1); });
