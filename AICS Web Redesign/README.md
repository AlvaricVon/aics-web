# AICS — AI customer service untuk UMKM Indonesia

Self-serve SaaS platform untuk multi-agent customer support. Frontend statis (HTML + CSS + Vanilla JS) yang deploy ke Vercel dan terhubung langsung ke Supabase (Postgres + Edge Functions di TypeScript/Deno).

Dibangun oleh **Kamil Alfaris** — solo founder, Jakarta.

---

## 📁 Struktur file

```
/index.html              Landing page (hero + live demo widget + pricing + FAQ)
/signup.html             Customer signup (Supabase Auth)
/dashboard.html          Customer dashboard (overview, KB, logs, embed, settings, billing)
/admin.html              Internal admin (noindex) — orders, audits, leads, demo chats
/widget.html             Embeddable chat widget (iframe target)
/chat.html               Standalone full-screen wrapper around widget.html
/reset-password.html     Password reset (request + set new)
/embed.js                1-line embed loader for customer websites (FAB + iframe)
/og-image.html           Social share card (open in browser → screenshot to PNG 1200×630)
/linkedin-banner.html    LinkedIn cover banner (open in browser → screenshot to PNG 1584×396)
/vercel.json             Vercel config: cleanUrls + /c/:slug redirect + cache headers
```

---

## 🔧 Setup

### 1. Deploy ke Vercel

```bash
# Connect repo (via Vercel CLI or web UI)
vercel
```

Tidak ada build step — semua file static, deploy langsung.

### 2. Configure Supabase

Set environment di Supabase dashboard:

- **URL**: `https://stcywvcnbbapshrzqblk.supabase.co`
- **Publishable key** (anon): `sb_publishable_WUxbFG3866P7BANLSqv-Sw_4NcXMLSr`

Key ini sudah di-hardcode di tiap halaman HTML. Aman karena publishable.

### 3. Edge Functions yang dipakai

| Function          | Path                                | Dipakai oleh              |
|-------------------|-------------------------------------|---------------------------|
| `cs-demo`         | `/functions/v1/cs-demo`             | Landing demo + widget     |
| `get_tenant_config` (RPC) | postgres function           | Widget (load brand/bot config) |

Setiap halaman punya **fallback lokal** kalau endpoint tidak reachable — demo widget tetap interaktif walau backend down.

---

## 🎨 Design system

### Palette (warm, professional — NOT default blue)

| Token             | Hex       |
|-------------------|-----------|
| Background        | `#FAFAF7` |
| Surface           | `#FFFFFF` |
| Surface alt       | `#F5F4F1` |
| Text primary      | `#1C1917` |
| Text soft         | `#44403C` |
| Muted             | `#78716C` |
| Border            | `#E7E5E4` |
| **Accent (CTA)**  | `#C2410C` (terracotta) |
| Accent hover      | `#9A3412` |
| Accent bg         | `#FFF7ED` |
| Success           | `#15803D` |
| Warning           | `#D97706` |
| Danger            | `#DC2626` |

### Typography

- **Display & body**: Plus Jakarta Sans (400/500/600/700/800)
- **Mono accents**: JetBrains Mono (400/500/600) — code, technical labels, status pills, numbers

Loaded from Google Fonts CDN.

### Component tokens

- Buttons: `border-radius: 7px`, padding `11px 16px`, hover lifts -1px dengan subtle orange shadow
- Cards: `border-radius: 10-14px`, 1px border, hover shadow ringan
- Status pills: monospace font, uppercase, 4px radius
- Modals: max 560px width, backdrop blur

---

## 🔌 Embed cara pasang

Customer cukup paste 1 baris ke websitenya:

```html
<script src="https://aics-web.vercel.app/embed.js" data-tenant="toko-anda" defer></script>
```

Atau standalone URL:

```
https://aics-web.vercel.app/c/toko-anda
```

`/c/:slug` di-redirect ke `/chat.html?t=:slug` via `vercel.json`.

---

## 🧩 Live demo widget (landing hero)

POST request ke `cs-demo` Edge Function:

```json
POST https://stcywvcnbbapshrzqblk.supabase.co/functions/v1/cs-demo
Header: apikey: sb_publishable_WUxbFG3866P7BANLSqv-Sw_4NcXMLSr
Body: { "message": "Status pesanan saya?", "session_id": "demo_abc123" }
```

Expected response shape:

```json
{
  "reply": "Pesanan #28471 sedang dalam pengiriman...",
  "state": "RESOLVED | ESCALATED | AWAITING_CUSTOMER",
  "intent": "order_status",
  "confidence": 0.94,
  "escalated": false
}
```

---

## 🖼 Social images

`og-image.html` dan `linkedin-banner.html` adalah template HTML yang bisa di-screenshot:

1. Buka file di browser
2. Set window/zoom sesuai dimensi (1200×630 atau 1584×396)
3. Screenshot → simpan sebagai PNG di root project

Sesudah itu OG meta tag di `index.html` otomatis pakai `og-image.png`.

---

## 🇮🇩 Voice / copy guidelines

- Formal-tapi-hangat: "kami" + "Anda"
- Sebut "UMKM" dan "startup Indonesia" secara natural
- Hindari jargon korporat ("synergize", "leverage")
- Pakai angka spesifik (`400+ chats handled`, bukan "many")
- Minimal emoji — hanya di tempat yang manusiawi (footer 🇮🇩, banner ⏰)

---

## 📜 License

MIT · © 2026 Kamil Alfaris
