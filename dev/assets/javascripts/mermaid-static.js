// Mounts the pre-rendered Mermaid diagrams that hooks/mermaid_static.py writes into the
// page, without inline style (the site's CSP has no 'unsafe-inline' in style-src).
// Each <div class="mermaid-static"> holds a <template> with the diagram's <link> and SVG.
// Like the theme, it goes into a closed shadow root, so the page's styles cannot reach
// the diagram. The style="" values Mermaid wrote travel as data-mmd-style and are applied
// through the CSSOM, which CSP does not govern. document$ fires on the first load and
// after every instant navigation.
document$.subscribe(function () {
  document.querySelectorAll("div.mermaid-static").forEach(function (host) {
    var template = host.querySelector(":scope > template");
    if (!template || host.dataset.mounted) return;
    host.dataset.mounted = "true";
    var root = host.attachShadow({ mode: "closed" });
    root.appendChild(document.importNode(template.content, true));
    root.querySelectorAll("[data-mmd-style]").forEach(function (el) {
      el.style.cssText = el.getAttribute("data-mmd-style");
      el.removeAttribute("data-mmd-style");
    });
  });
});
