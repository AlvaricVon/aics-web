// AICS Embed Script — 1-line install
// Usage on customer's website:
// <script src="https://aics-web.vercel.app/embed.js" data-tenant="your-slug"></script>
(function () {
  "use strict";

  // Get tenant slug from script tag
  const currentScript = document.currentScript || (function () {
    const scripts = document.getElementsByTagName("script");
    return scripts[scripts.length - 1];
  })();
  const tenant = currentScript?.getAttribute("data-tenant") || currentScript?.dataset?.tenant;
  const baseUrl = "https://aics-web.vercel.app";

  if (!tenant) {
    console.warn("[AICS] data-tenant attribute missing on embed script.");
    return;
  }

  // ===== Styles =====
  const style = document.createElement("style");
  style.textContent = `
    .aics-fab {
      position: fixed;
      bottom: 24px;
      right: 24px;
      width: 56px;
      height: 56px;
      border-radius: 50%;
      background: #C2410C;
      box-shadow: 0 8px 24px rgba(0,0,0,0.18);
      cursor: pointer;
      display: flex;
      align-items: center;
      justify-content: center;
      z-index: 2147483646;
      border: none;
      transition: transform 0.2s, box-shadow 0.2s;
    }
    .aics-fab:hover { transform: translateY(-3px); box-shadow: 0 12px 28px rgba(0,0,0,0.22); }
    .aics-fab svg { width: 26px; height: 26px; fill: white; }
    .aics-fab .aics-badge {
      position: absolute;
      top: -3px; right: -3px;
      background: #DC2626;
      color: white;
      font-size: 10px;
      font-weight: 700;
      width: 18px; height: 18px;
      border-radius: 50%;
      display: none;
      align-items: center;
      justify-content: center;
      font-family: -apple-system, sans-serif;
    }
    .aics-fab .aics-badge.show { display: flex; }
    .aics-frame-wrap {
      position: fixed;
      bottom: 92px;
      right: 24px;
      width: 380px;
      height: 560px;
      max-height: calc(100vh - 120px);
      border-radius: 14px;
      overflow: hidden;
      box-shadow: 0 20px 60px rgba(0,0,0,0.22);
      z-index: 2147483645;
      display: none;
      transform: translateY(10px) scale(0.96);
      opacity: 0;
      transition: transform 0.22s ease-out, opacity 0.22s ease-out;
      background: white;
    }
    .aics-frame-wrap.open {
      display: block;
      transform: translateY(0) scale(1);
      opacity: 1;
    }
    .aics-frame-wrap iframe {
      width: 100%;
      height: 100%;
      border: 0;
      display: block;
    }
    @media (max-width: 480px) {
      .aics-frame-wrap {
        width: calc(100vw - 24px);
        right: 12px;
        bottom: 84px;
        height: calc(100vh - 110px);
      }
      .aics-fab { right: 16px; bottom: 16px; }
    }
  `;
  document.head.appendChild(style);

  // ===== FAB button =====
  const fab = document.createElement("button");
  fab.className = "aics-fab";
  fab.setAttribute("aria-label", "Buka chat support");
  fab.innerHTML = `
    <svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
      <path d="M20 2H4c-1.1 0-1.99.9-1.99 2L2 22l4-4h14c1.1 0 2-.9 2-2V4c0-1.1-.9-2-2-2zm-2 12H6v-2h12v2zm0-3H6V9h12v2zm0-3H6V6h12v2z"/>
    </svg>
    <span class="aics-badge">1</span>
  `;
  document.body.appendChild(fab);

  // ===== Iframe wrap =====
  const wrap = document.createElement("div");
  wrap.className = "aics-frame-wrap";
  wrap.setAttribute("role", "dialog");
  wrap.setAttribute("aria-label", "Chat with support");
  const iframe = document.createElement("iframe");
  iframe.src = `${baseUrl}/widget.html?t=${encodeURIComponent(tenant)}`;
  iframe.setAttribute("allow", "clipboard-write");
  iframe.setAttribute("title", "AICS Chat Widget");
  wrap.appendChild(iframe);
  document.body.appendChild(wrap);

  let open = false;
  function toggle() {
    open = !open;
    wrap.classList.toggle("open", open);
    if (open) {
      document.querySelector(".aics-badge")?.classList.remove("show");
    }
  }
  fab.addEventListener("click", toggle);

  // ===== Listen messages from widget =====
  window.addEventListener("message", (e) => {
    if (e.data?.type === "aics:close") {
      open = false;
      wrap.classList.remove("open");
    }
  });

  // ===== Public API =====
  window.AICS = {
    open: () => { if (!open) toggle(); },
    close: () => { if (open) toggle(); },
    toggle,
    version: "1.0.0",
    tenant,
  };
})();
