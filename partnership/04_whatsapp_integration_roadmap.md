# AICS — WhatsApp Integration Roadmap

> **Owner:** Alvin Zaidan (lead dev) + Kamil (architecture review)
> **Target launch:** Q3 2026 (target 2 minggu development sprint setelah Meta approval, biasa makan 2-4 minggu)
> **Status:** PLANNING — belum dimulai
> **Version:** 1.0 · May 2026

---

## 1. Kenapa Ini Critical

Realita pasar Indonesia (data Mei 2026):
- **~85% UMKM digital** main di marketplace (Shopee, Tokopedia, Lazada, TikTok Shop) — gak punya website sendiri
- **~90% UMKM digital** pakai **WhatsApp Business** sebagai channel CS utama
- Marketplace chat API (Shopee/Tokped) **tertutup** untuk third-party — kita gak bisa integrate
- Tapi semua marketplace seller tetap **redirect customer ke WhatsApp** untuk pertanyaan kompleks

**Implication:**
Tanpa WhatsApp integration, total addressable market AICS = ~10-15% bisnis digital Indonesia (yang punya website).
Dengan WhatsApp integration = TAM melonjak ke ~85-90% bisnis digital Indonesia.

**Konversi simpel:**
```
Tanpa WA:  Target = 50.000 D2C brand + startup dengan website
Dengan WA: Target = 50.000 + 64 juta UMKM aktif di WA Business
```

Itu sebabnya WhatsApp integration = **highest-leverage feature** yang bisa dibangun.

---

## 2. Architecture Overview

```
┌─────────────────────────────────────────────────────────┐
│  Customer (UMKM) kirim pesan ke nomor WA Business      │
│                                                          │
│  Contoh: "Kak kapan paket gw sampe?"                    │
└────────────────────────────┬────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────┐
│  Meta WhatsApp Cloud API (webhook ke AICS)             │
│  POST https://aics.supabase.co/functions/v1/wa-inbox    │
└────────────────────────────┬────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────┐
│  Supabase Edge Function: wa-inbox                       │
│  1. Verify Meta signature                                │
│  2. Lookup tenant by phone_number_id                    │
│  3. Forward ke tenant-chat function (existing)           │
│  4. Get AI response                                      │
│  5. POST balik ke Meta WhatsApp Cloud API               │
└────────────────────────────┬────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────┐
│  Customer dapet auto-reply dalam <3 detik               │
└─────────────────────────────────────────────────────────┘
```

**Komponen yang harus dibangun:**
1. ✨ Edge function baru: `wa-inbox` (webhook receiver)
2. ✨ Edge function baru: `wa-send` (outbound sender)
3. ✨ Tabel baru: `wa_phone_numbers` (mapping tenant_id ↔ phone_number_id)
4. ✨ Dashboard UI baru: WhatsApp setup wizard
5. 🔁 Reuse existing: `tenant-chat`, KB, multi-agent logic — gak perlu rewrite

---

## 3. Meta Business Cloud API — Setup Steps

> **Yang harus dikerjain Kamil (sebagai owner business):**

### Step 1: Verify Meta Business Account (1-3 hari)
1. Buka [business.facebook.com](https://business.facebook.com)
2. Buat Business Account "AICS Indonesia" (kalau belum)
3. Verify business dengan dokumen:
   - NIB (Nomor Induk Berusaha) — bisa daftar di oss.go.id gratis kalau belum punya
   - NPWP usaha
   - Akta pendirian (kalau PT) atau Surat Keterangan Usaha (kalau perorangan)
4. Tunggu Meta review (1-3 hari biasa)

### Step 2: Setup WhatsApp Business Platform (30 menit)
1. Di Meta Business Suite → menu **WhatsApp Manager**
2. Add WhatsApp Business Account (WABA)
3. Add phone number untuk AICS production:
   - **Option A (recommended):** Pakai nomor baru khusus (beli SIM card / virtual number)
   - **Option B:** Nomor existing yang **bukan** terdaftar di app WhatsApp consumer
4. Verify dengan SMS / call
5. Setup display name: "AICS Customer Support" (Meta review 1-2 hari)

### Step 3: Generate Access Token (10 menit)
1. Buka [developers.facebook.com](https://developers.facebook.com) → App lu
2. WhatsApp → Configuration → Permanent Access Token
3. Save tokennya di Supabase secrets:
   ```bash
   supabase secrets set WA_ACCESS_TOKEN=EAAxxxx...
   supabase secrets set WA_PHONE_NUMBER_ID=12345...
   supabase secrets set WA_BUSINESS_ACCOUNT_ID=67890...
   supabase secrets set WA_WEBHOOK_VERIFY_TOKEN=$(openssl rand -hex 16)
   ```

### Step 4: Configure Webhook (15 menit)
1. WhatsApp → Configuration → Webhooks
2. Callback URL: `https://[project].supabase.co/functions/v1/wa-inbox`
3. Verify token: yang udah lu generate di Step 3
4. Subscribe fields: `messages`, `message_status`

### Step 5: Test Conversation (30 menit)
1. Send test message ke nomor AICS dari WA pribadi
2. Cek logs di Supabase function dashboard
3. Verify balasan AI sampe ke customer

---

## 4. Development Sprint Plan (Alvin lead)

### Week 1: Foundation (10-15 jam total)

**Day 1-2: Schema + Edge Function skeleton**
- ☐ Tambah tabel `wa_phone_numbers`:
  ```sql
  create table public.wa_phone_numbers (
    id uuid primary key default gen_random_uuid(),
    tenant_id uuid not null references public.tenants(id) on delete cascade,
    phone_number_id text not null unique,  -- dari Meta
    display_phone text not null,            -- 6281234567890
    waba_id text not null,
    status text default 'pending',          -- pending|verified|active|suspended
    created_at timestamptz default now()
  );
  alter table public.wa_phone_numbers enable row level security;
  ```
- ☐ Buat edge function `wa-inbox` (webhook receiver — GET untuk verify, POST untuk message)
- ☐ Test dengan ngrok / Supabase deployment

**Day 3-4: Inbound message flow**
- ☐ Parse WhatsApp message payload
- ☐ Lookup tenant by `phone_number_id`
- ☐ Forward ke existing `tenant-chat` function (reuse logic)
- ☐ Handle attachment (image/document) — Phase 1 baca caption aja, attachment forwarding Phase 2

**Day 5: Outbound message**
- ☐ Buat edge function `wa-send`
- ☐ Call Meta Cloud API: `POST graph.facebook.com/v18.0/{phone_number_id}/messages`
- ☐ Handle text response (Phase 1) + template message (Phase 2)
- ☐ Log message status ke tabel `messages` (existing) dengan field `channel = 'whatsapp'`

### Week 2: Dashboard UI + Polish (10-15 jam total)

**Day 6-7: Dashboard WhatsApp setup wizard**
- ☐ Tambah halaman `/dashboard/whatsapp.html`
- ☐ Step-by-step wizard:
  1. Connect Meta Business Account (OAuth flow Meta — research dulu)
  2. Pilih WhatsApp Business Account
  3. Pilih phone number
  4. Verify webhook setup
  5. Test message

**Day 8: Notifikasi + Monitoring**
- ☐ Dashboard tampilan: total WA messages received/sent per hari
- ☐ Alert kalau Meta API error (rate limit, token expired)

**Day 9-10: Documentation + Sales material**
- ☐ Tulis docs customer: "Cara connect WhatsApp ke AICS"
- ☐ Update landing page: hapus "WhatsApp coming Q2" → ganti "WhatsApp + Website tersedia"
- ☐ Update pricing: tier WhatsApp = +Rp 100rb/bulan (atau bundled di Pro tier?)

---

## 5. Pricing Strategy (Pasca-Launch WA)

**Opsi 1: WhatsApp = premium add-on**
- Starter (Rp 99rb): web chat only
- Pro (Rp 299rb): web chat + WhatsApp (1 nomor)
- Business (Rp 999rb): web chat + WhatsApp (3 nomor) + branding hapus

**Opsi 2: WhatsApp di semua tier (limit by volume)**
- Starter (Rp 99rb): 500 WA msg/bln
- Pro (Rp 299rb): 5,000 WA msg/bln
- Business (Rp 999rb): unlimited

**Rekomendasi:** Opsi 2. Alasannya — WhatsApp = differentiator vs Cekat/Wati yang charge mahal. Bikin entry barrier rendah, customer convert ke higher tier saat volume naik.

> **Catatan biaya Meta:** Conversation pricing Meta = $0.005–0.06 per conversation (24 jam window). Untuk 5,000 conversations/bulan = ~$25-300. Margin masih sehat di Pro tier.

---

## 6. Sales Positioning (Pre vs Post Launch)

### SEKARANG (Pre-WA, May-July 2026):
- Target: D2C brand + startup dengan website
- Pitch: "AI customer support untuk website Anda, 5 menit setup"
- **JANGAN promise** WhatsApp ke prospect kecuali sebagai "coming soon Q3" → bisa convert ke waiting list

### POST-LAUNCH (Q3 2026 onward):
- Target: D2C brand + UMKM marketplace seller + service business
- Pitch: "AI customer support multi-channel (Web + WhatsApp), 1 setup, all channels"
- **Killer differentiator:** "Satu-satunya platform lokal Indonesia dengan harga mulai Rp 99rb yang udah include WhatsApp + Web AI customer support"

### Migration messaging untuk existing customer:
- Email + dashboard notification: "🎉 WhatsApp integration sekarang available! Aktivasi sekarang gratis selama Q3 (normal price Rp 100rb)"
- Limited-time bonus: customer existing dapet quota 2x lipat selama 3 bulan setelah aktivasi WA

---

## 7. Risk & Mitigation

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| Meta business verification rejected | Medium | High | Siapin dokumen lengkap dari awal (NIB, NPWP, akta). Backup: pakai third-party BSP (Twilio, MessageBird) yang udah pre-verified |
| Meta API rate limit | Medium | Medium | Queue system di edge function, exponential backoff. Untuk volume tinggi, upgrade tier Meta |
| Phone number suspended | Low | Critical | Patuh policy: no spam, opt-in based, response time <24h. Setup monitoring alert |
| Cost meledak (Meta charge per conversation) | Medium | Medium | Hard limit per tenant di edge function. Notify customer kalau approaching limit. Bill overage transparan |
| Customer expect SLA tinggi (multi-channel = lebih critical) | High | Medium | TOS clear: best-effort, no 99.9% SLA at current pricing. Upsell ke Business tier untuk SLA |
| Alvin masih kerja Indocyber, dev velocity slow | High | Medium | Buffer 2x waktu estimasi. Kamil bantu code review + testing. Kalau timeline meleset → tunda launch, jangan launch buggy |

---

## 8. Success Metrics (90 hari post-launch)

| Metric | Target Q3 end | Target Q4 end |
|---|---|---|
| Customer aktivasi WA | 30% existing | 60% existing |
| New signup yang choose WA | 50% new signup | 70% new signup |
| WA messages processed/bulan | 50,000 | 250,000 |
| Trial-to-paid conversion | 12% → 18% | 18% → 25% |
| Avg revenue per customer | Rp 220rb | Rp 320rb |
| Total MRR contribution dari WA | Rp 10jt | Rp 50jt |

---

## 9. Dependencies & Blockers

**Yang harus selesai DULU sebelum sprint dimulai:**
1. ✅ Kamil verify Meta Business Account (kerja paralel — bisa sambil Alvin setup dev environment)
2. ✅ Alvin baca dokumentasi Meta WhatsApp Cloud API: [developers.facebook.com/docs/whatsapp/cloud-api](https://developers.facebook.com/docs/whatsapp/cloud-api) (2-3 jam)
3. ✅ Decide pricing model (Kamil decision)
4. ✅ Buy / siapkan nomor WhatsApp khusus untuk AICS production

**Yang bisa parallel (gak block):**
- Marketing collateral baru (post-launch)
- Updated demo video
- Customer onboarding docs

---

## 10. Communication Protocol Selama Sprint

- **Daily Slack/WA check-in:** Alvin post progress harian (5-10 menit)
- **Code review:** Kamil review setiap PR Alvin sebelum merge (max 24 jam turnaround)
- **Weekly Zoom:** Sabtu sore 1 jam — demo progress + unblock issues
- **Emergency escalation:** WA Kamil langsung kalau Meta API issue / blocked

---

## 11. Post-Launch Action Plan (Week 1 setelah live)

- ☐ Soft launch ke 5 existing customer (gratis)
- ☐ Collect feedback intensive (1-on-1 call masing-masing)
- ☐ Fix critical bugs (target 48 jam resolution)
- ☐ Hard launch via LinkedIn + email blast existing waiting list
- ☐ Update sales pitch deck semua channel
- ☐ Press release ke media startup Indonesia (DailySocial, TechInAsia, etc.)

---

## 12. Long-term Vision (Q4 2026 onward)

**Phase 2 (post WhatsApp basic):**
- WhatsApp template message untuk proactive notification (order confirmation, shipping update)
- WhatsApp catalog integration (showcase produk in-chat)
- WhatsApp Flow (interactive form)
- Multi-agent handoff: AI handle 80% → escalate ke human via WA web app

**Phase 3 (2027):**
- Instagram DM integration (Meta — same Cloud API)
- Telegram Bot integration
- Tokopedia/Shopee chat (KALAU mereka buka API — possible setelah regulator push)

---

*Document version: 1.0 · Created: May 2026 · Owners: Kamil (architecture) + Alvin (lead dev)*
