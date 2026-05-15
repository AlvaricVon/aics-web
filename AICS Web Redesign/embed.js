/* AICS chat widget embed loader
 * Usage: <script src="https://aics-web.vercel.app/embed.js" data-tenant="your-slug" defer></script>
 *
 * Creates a floating action button (FAB) bottom-right.
 * On click, toggles an iframe loading widget.html?t=<tenant>.
 * All styles injected via JS (no global CSS conflict).
 * PostMessage protocol: child posts {type:'aics:close'} to dismiss.
 */
(function () {
  if (window.__aics_embedded) return;
  window.__aics_embedded = true;

  // ─── Read config ───
  var script = document.currentScript ||
    (function () {
      var s = document.getElementsByTagName('script');
      return s[s.length - 1];
    })();
  var tenant = (script && script.getAttribute('data-tenant')) || 'demo';
  var brandColor = (script && script.getAttribute('data-color')) || '#C2410C';
  var origin = (function () {
    try { return new URL(script.src).origin; }
    catch (e) { return 'https://aics-web.vercel.app'; }
  })();
  var label = (script && script.getAttribute('data-label')) || 'Chat support';

  // ─── Inject CSS (scoped to .aics-* classes) ───
  var style = document.createElement('style');
  style.id = 'aics-embed-style';
  style.textContent = [
    '.aics-fab{',
    '  position:fixed;bottom:20px;right:20px;z-index:2147483646;',
    '  width:58px;height:58px;border-radius:50%;',
    '  background:' + brandColor + ';color:#fff;cursor:pointer;border:none;',
    '  display:flex;align-items:center;justify-content:center;',
    '  box-shadow:0 8px 24px rgba(0,0,0,.18),0 2px 6px rgba(0,0,0,.10);',
    '  transition:transform .18s cubic-bezier(.34,1.4,.6,1),box-shadow .18s;',
    '  font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;',
    '}',
    '.aics-fab:hover{transform:scale(1.06);box-shadow:0 12px 32px rgba(0,0,0,.22),0 2px 6px rgba(0,0,0,.10)}',
    '.aics-fab svg{width:26px;height:26px;color:#fff;transition:transform .25s ease}',
    '.aics-fab.aics-open svg.aics-icon-chat{transform:scale(0) rotate(-90deg)}',
    '.aics-fab.aics-open svg.aics-icon-close{transform:scale(1) rotate(0)}',
    '.aics-fab svg.aics-icon-close{position:absolute;transform:scale(0) rotate(90deg)}',
    '.aics-fab .aics-dot{',
    '  position:absolute;top:6px;right:6px;width:12px;height:12px;border-radius:50%;',
    '  background:#15803D;border:2px solid #fff;',
    '}',
    '.aics-fab.aics-open .aics-dot{display:none}',

    '.aics-iframe-wrap{',
    '  position:fixed;bottom:90px;right:20px;z-index:2147483645;',
    '  width:380px;height:600px;max-width:calc(100vw - 40px);max-height:calc(100vh - 110px);',
    '  background:#fff;border-radius:14px;overflow:hidden;',
    '  box-shadow:0 24px 64px -8px rgba(0,0,0,.28),0 4px 12px rgba(0,0,0,.10);',
    '  opacity:0;transform:translateY(20px) scale(.96);transform-origin:bottom right;',
    '  pointer-events:none;transition:opacity .22s ease,transform .22s cubic-bezier(.34,1.2,.6,1);',
    '}',
    '.aics-iframe-wrap.aics-open{opacity:1;transform:translateY(0) scale(1);pointer-events:auto}',
    '.aics-iframe-wrap iframe{width:100%;height:100%;border:none;display:block;background:#FAFAF7}',

    '@media (max-width:520px){',
    '  .aics-iframe-wrap{bottom:0;right:0;width:100vw;height:100vh;max-width:100vw;max-height:100vh;border-radius:0}',
    '  .aics-fab{bottom:16px;right:16px}',
    '}',
  ].join('\n');
  document.head.appendChild(style);

  // ─── Build FAB ───
  var fab = document.createElement('button');
  fab.className = 'aics-fab';
  fab.type = 'button';
  fab.setAttribute('aria-label', label);
  fab.innerHTML =
    '<svg class="aics-icon-chat" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 11.5a8.38 8.38 0 0 1-.9 3.8 8.5 8.5 0 0 1-7.6 4.7 8.38 8.38 0 0 1-3.8-.9L3 21l1.9-5.7a8.38 8.38 0 0 1-.9-3.8 8.5 8.5 0 0 1 4.7-7.6 8.38 8.38 0 0 1 3.8-.9h.5a8.48 8.48 0 0 1 8 8v.5z"/></svg>' +
    '<svg class="aics-icon-close" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round"><line x1="6" y1="6" x2="18" y2="18"/><line x1="6" y1="18" x2="18" y2="6"/></svg>' +
    '<span class="aics-dot"></span>';

  // ─── Build iframe wrap (lazy mount on first open) ───
  var wrap = document.createElement('div');
  wrap.className = 'aics-iframe-wrap';
  var iframe = null;
  var open = false;

  function toggle() {
    open = !open;
    if (open && !iframe) {
      iframe = document.createElement('iframe');
      iframe.title = 'AICS chat';
      iframe.allow = 'clipboard-write';
      iframe.src = origin + '/widget.html?t=' + encodeURIComponent(tenant);
      wrap.appendChild(iframe);
    }
    fab.classList.toggle('aics-open', open);
    wrap.classList.toggle('aics-open', open);
  }

  fab.addEventListener('click', toggle);

  // ─── Listen for child close requests ───
  window.addEventListener('message', function (e) {
    if (!e.data || typeof e.data !== 'object') return;
    if (e.data.type === 'aics:close' && open) toggle();
  });

  // ─── Mount when DOM ready ───
  function mount() {
    document.body.appendChild(wrap);
    document.body.appendChild(fab);
  }
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', mount);
  } else {
    mount();
  }

  // ─── Public API ───
  window.AICS = {
    open: function () { if (!open) toggle(); },
    close: function () { if (open) toggle(); },
    toggle: toggle,
    tenant: tenant
  };
})();
