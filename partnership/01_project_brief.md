# AICS — Project Brief

**Untuk:** Alvin Zaidan Faizal Putra (Growth Partner)
**Dari:** Kamil Alfaris (Founder & CEO)
**Status:** Active — Day 1 launch

---

## 1. Apa Itu AICS?

**AICS adalah platform AI customer support self-serve untuk D2C brands, SaaS, dan online business Indonesia yang punya website.**

> ⚠️ **PENTING**: Target market kami **bukan** UMKM warung kecil yang jualan di Tokopedia/Shopee/Lazada (kami belum bisa integrate marketplace chat). Target kami = brand/business yang sudah punya website sendiri.
>
> **WhatsApp Business integration**: dalam roadmap 2-4 minggu (Alvin lead).

### Problem yang kami selesaikan:
- Owner D2C brand/startup yang punya website kewalahan handle FAQ berulang via web chat + WhatsApp
- Agency AI lokal charge Rp 200jt+ untuk implementasi (terlalu mahal)
- SaaS chatbot existing (Cekat, Wati, Qontak) terlalu kaku + mahal (Rp 600rb–2,5jt/bulan)
- Banyak yang butuh middle ground: affordable + flexible + self-serve

### Solusi:
- Platform self-serve yang customer bisa pasang chatbot AI di website mereka **dalam 5 menit**
- Custom knowledge base sendiri (mereka isi sendiri)
- Custom branding (warna, nama bot, sambutan)
- Mulai **Rp 99rb/bulan** (jauh lebih murah dari kompetitor)
- Trial 14 hari gratis (no kartu kredit)

### Target audience (TIER A — fokus prioritas):
- ✅ **D2C brands** dengan website sendiri (Erigo, Compass, Buttonscarves, AVO, BLP Beauty, Sociolla style)
- ✅ **F&B chains** dengan own app/web (Kopi Kenangan, Janji Jiwa, Fore)
- ✅ **SaaS startups** Indonesia mid-stage (Mekari, Qoala, Sirka, Hangry)
- ✅ **Edu platform** dengan website (Skill Academy, Cakap, Ruangguru sub-products)
- ✅ **Klinik/dokter** dengan website appointment booking
- ✅ **Solopreneur** dengan landing page (konsultan, coach, course creator)

### BUKAN target audience (untuk sekarang):
- ❌ Warung online di Instagram tanpa website
- ❌ Seller Tokopedia/Shopee/Lazada tanpa website sendiri (chat marketplace API tertutup, kami gak bisa integrate)
- ❌ UMKM offline tanpa digital presence
- ❌ Enterprise besar dengan tim 50+ CS (mereka butuh agency Rp 200jt+ + dedicated team)

### Setelah WhatsApp integration live (Q2):
- ✅ **UMKM yang pakai WhatsApp Business** sebagai channel utama (90% UMKM Indonesia) — market akan terbuka 10x lebih besar

---

## 2. Stack Teknis

| Layer | Tech | Note |
|---|---|---|
| Frontend | HTML + CSS + Vanilla JS | Static, no build step |
| Hosting | Vercel (free tier) | Auto-deploy from GitHub |
| Backend | Supabase Postgres + Edge Functions (Deno/TypeScript) | Free tier cukup untuk ~50 customer |
| LLM | Groq (free) → Anthropic Claude (paid nanti) | Llama 3.3 70B saat ini |
| Auth | Supabase Auth (email + password + magic link) | |
| Repo | github.com/AlvaricVon/aics-web | |
| Live URL | https://aics-web.vercel.app | |

---

## 3. Pricing & Plan

| Plan | Harga | Limit pesan | Channel | Features |
|---|---|---|---|---|
| Trial | Gratis 14 hari | 100 msg | 1 | Full features |
| **Lite** | **Rp 99.000/bulan** | 500 msg | 1 | Basic dashboard |
| **Pro** ⭐ | **Rp 299.000/bulan** | 3.000 msg | 3 | Full features + analytics |
| **Business** | **Rp 999.000/bulan** | Unlimited | Unlimited | Priority support |
| Custom | Rp 15jt+ | Custom | Custom | Full integration build |

**Target main = Pro plan.** Lite untuk akuisisi, Business untuk yang scaling.

---

## 4. Cara Setup (untuk customer baru)

### Customer journey 5 menit:

```
1. Customer buka https://aics-web.vercel.app
   ↓
2. Klik "Mulai trial 14 hari"
   ↓
3. Isi form: company name, slug (URL chatbot), email, password
   ↓
4. Konfirmasi email (klik link yang dikirim)
   ↓
5. Login ke /dashboard
   ↓
6. Tab "Knowledge Base" → add artikel (mereka sudah dapat 3 starter)
   ↓
7. Tab "Settings" → customize branding (warna, nama bot, sambutan)
   ↓
8. Tab "Embed Code" → copy 1 baris script
   ↓
9. Paste di website mereka sebelum </body>
   ↓
10. SELESAI — chatbot live di website mereka
```

### Setelah trial 14 hari:
- Customer klik tab "Billing" → pilih plan
- Modal muncul dengan detail transfer bank BCA 683-129-7252 a.n. Kamil Alfaris
- Customer transfer, konfirmasi via WA: wa.me/6281293988757
- Kamil approve di /admin → status berubah ke "paid", plan aktif

---

## 5. Channel yang Supported

| Channel | Status | ETA |
|---|---|---|
| **Website embed** (HTML, Shopify, WordPress, Webflow) | ✅ READY | — |
| **Standalone share link** (untuk yang gak punya web) | ✅ READY | — |
| **WhatsApp Business API** | ❌ Belum | Q2-Q3 2026 (Alvin's domain) |
| **Instagram DM** | ❌ Belum | Q3-Q4 2026 |
| **Tokopedia/Shopee chat** | ❌ Tidak bisa | API mereka tertutup |
| **Telegram Bot** | ❌ Belum | Bisa cepat (1 minggu work) |

---

## 6. Competitive Positioning

| Kompetitor | Harga | Pros | Cons |
|---|---|---|---|
| **Cekat.ai** | Rp 850rb-2,5jt/bln | Established, multi-channel | Mahal, lock-in |
| **Wati** | Rp 600rb+ | WhatsApp specialist | Cuma WA, gak ada AI custom |
| **Qontak** | Rp 1jt+ | Enterprise grade | Overkill untuk brand kecil-medium |
| **Manychat** | Rp 250rb+ (USD) | Easy setup | Rule-based, gak ada AI grounded |
| **AICS** | **Rp 99rb-999rb** | Affordable, self-serve, AI grounded with KB | Belum ada WA integration (yet), founder-led brand belum established |

**Selling point AICS:**
1. **Harga paling murah** di kategori AI chatbot Indonesia
2. **Self-serve** — gak butuh sales call, customer pasang sendiri
3. **AI grounded dengan KB** customer (no hallucination)
4. **Source code transparan** (GitHub public)
5. **Personal touch founder-led** (Kamil direct via WhatsApp)

---

## 7. ✅ Kelebihan AICS

- **Affordable**: 5-10x lebih murah dari Cekat/Wati/Qontak
- **Self-serve**: customer bisa pasang sendiri tanpa sales call
- **Multi-tenant**: setiap customer punya workspace terpisah dengan KB sendiri
- **Custom branding**: warna, nama bot, sambutan bisa diubah customer
- **Trial 14 hari** tanpa kartu kredit (low friction signup)
- **AI grounded with KB** (jawaban dari knowledge base customer, bukan halu)
- **Auto escalation** untuk kasus abusive/legal (safety net)
- **Source code di GitHub** (transparansi, customer bisa audit)
- **Real-time admin dashboard** untuk monitor leads/orders/chats
- **Built dengan stack modern** (Supabase + Vercel + Groq) — scalable

## ⚠️ Kekurangan AICS (HONEST disclosure)

- **Founder masih solo + new** — 0 paying customer di awal, gak ada case study
- **Belum ada WhatsApp integration** — perlu Phase 2 (Alvin akan handle)
- **Belum support marketplace chat** (Tokopedia/Shopee) — API mereka tertutup
- **Free trial pakai Groq** — quality bagus tapi gak sebagus Claude (paid)
- **Email confirmation via Supabase free tier** — kadang masuk spam
- **Manual billing** — customer transfer bank → konfirmasi WA → admin approve (belum auto via Xendit/Midtrans)
- **Belum ada mobile native app** — web-only (responsive design tapi tetap web)
- **Trust factor rendah** karena brand baru — butuh testimonial pertama untuk bangun social proof
- **Dashboard UX masih basic** — polish iteration butuh waktu
- **Belum compliant SOC 2 / ISO** — UU PDP comply tapi belum sertifikasi formal

---

## 8. Sales Process (0 → Paid Customer)

```
PHASE 1: Discover (Week 1)
├─ Identify prospect (LinkedIn, komunitas D2C founder, referral)
├─ Research profile (15 menit per prospect)
└─ Compose personalized DM (value-first, no hard pitch)

PHASE 2: Engage (Week 1-2)
├─ Send DM
├─ Follow up 3 hari kemudian kalau no reply
└─ Offer free audit / demo specific untuk bisnis mereka

PHASE 3: Discovery Call (Week 2)
├─ 30 menit Zoom/Meet
├─ Pakai questionnaire untuk extract pain point
└─ Tunjuk demo live, jelaskan use case mereka

PHASE 4: Trial Signup (Week 2-3)
├─ Kirim signup link via WhatsApp
├─ Walk-through onboarding (KB add, embed code)
└─ Set up reminder check-in di hari ke-7 trial

PHASE 5: Conversion (Week 3-4)
├─ Hari ke-12 trial: personal WA "gimana experience-nya?"
├─ Show metric/progress (chat handled, deflection rate)
├─ Offer Lite dengan diskon 20% bulan pertama (Rp 79rb)
└─ Send invoice + bank detail

PHASE 6: Onboarding (After payment)
├─ Konfirmasi payment di /admin
├─ Aktivasi plan
└─ Welcome WhatsApp + tutorial video
```

**Expected conversion rate:** 
- 100 DM → 15 reply → 5 trial → 1-2 paid (industry standard B2B SaaS)
- First conversion: bulan ke-1
- Stabil 2-3 conversion/bulan: bulan ke-3

---

## 9. Roles & Responsibilities

### Kamil Alfaris (Founder & CEO)
- Strategi product + roadmap
- Build new features (code)
- Sales call + onboarding
- Customer success
- Financial management
- **80% effort marketing/sales sekarang**

### Alvin Zaidan Faizal Putra (Growth Partner — 10-15 jam/minggu)
- Content engagement di LinkedIn (cyber/tech niche)
- Refer ke network sendiri (IDN Boarding, Indocyber, networking community)
- DM outreach (volume lebih kecil, 30-50/bulan)
- **20% effort marketing**
- **Phase 2 (Bulan 3+):** Build WhatsApp Business API integration

### Compensation Alvin
- **Commission per customer** (recurring 3 bulan dari customer dia bawa):
  - Customer Lite (Rp 99rb) → Alvin dapat **Rp 10rb/bulan** × 3 bulan = Rp 30rb total
  - Customer Pro (Rp 299rb) → **Rp 30rb/bulan** × 3 = Rp 90rb total
  - Customer Business (Rp 999rb) → **Rp 100rb/bulan** × 3 = Rp 300rb total
  - Custom service Rp 15jt+ → **15% commission** sekali bayar

### Path to Co-founder (90 hari)
- Kalau Alvin bawa **minimum 5 paying customer** dalam 90 hari
- Naik ke **Technical Co-Founder** dengan **15-20% equity** vested over 3 tahun
- Focus shift ke build WhatsApp + Instagram + multi-channel integration

---

## 10. Tools & Akses yang Alvin Butuh

| Tool | URL | Akses |
|---|---|---|
| Live web | https://aics-web.vercel.app | Public |
| Demo (sebagai user) | Coba widget di hero | Public |
| Lead tracking sheet | Google Sheets (Kamil share link) | Edit access |
| LinkedIn engagement target | Sheet listing 50 prospect | Edit access |
| WhatsApp group AICS | (Kamil bikin) | Member |
| Daily standup | WhatsApp 1-on-1 dengan Kamil | — |

---

## 11. KPI Bulanan untuk Alvin

| Metric | Target Bulan 1 | Target Bulan 2 | Target Bulan 3 |
|---|---|---|---|
| DM personalized sent | 30 | 40 | 50 |
| LinkedIn post engagement (comment di post orang) | 30 (1/hari) | 30 | 30 |
| LinkedIn post sendiri | 4 (1/minggu) | 4 | 4 |
| Reply rate | 10-15% (3-5 reply) | 15-20% | 20%+ |
| Demo call booked | 1-2 | 2-3 | 3-5 |
| **Trial signup** | 0-1 | 1-2 | 2-3 |
| **Paying customer** | 0 | 0-1 | 1-2 |
| **Cumulative paying (90 hari)** | — | — | **Target: 5+** |

Kalau hit 5+ → naik ke Co-founder dengan equity.

---

## 12. Channel Komunikasi

- **WhatsApp 1-on-1** dengan Kamil (daily check)
- **Weekly Zoom** Senin pagi 30 menit (review metric, plan minggu)
- **Group WhatsApp AICS** (kalau partnership grown jadi 2+ orang)

---

## 13. Onboarding Steps untuk Alvin

1. ☐ Baca dokumen ini sampai habis
2. ☐ Akses live web https://aics-web.vercel.app — test demo widget
3. ☐ Update LinkedIn profile (lihat dokumen `03_alvin_todo_list.md`)
4. ☐ Diskusi dengan Kamil — clarify questions
5. ☐ Setup Google Sheet lead tracking (dapat link dari Kamil)
6. ☐ Mulai Day 1 outreach plan (lihat dokumen todo list)

---

## 14. FAQ Internal

**Q: Kalau ada customer tanya bisa pasang di WhatsApp gak?**
A: Sekarang BELUM. Roadmap Q2-Q3. Untuk sekarang AICS untuk website. Kalau prospect insist WA, refer ke Wati / Cekat (be honest), tapi tanya juga — apakah mereka punya website juga? Karena kalau iya, kita bisa pasang di website mereka dulu sambil tunggu WA integration.

**Q: Kalau customer mau custom features?**
A: Tier Custom (Rp 15jt+). Tapi sebagai Growth Partner, fokus ke Lite/Pro dulu. Custom = lead untuk Kamil close.

**Q: Kalau customer tanya source code?**
A: Source code publik di github.com/AlvaricVon/aics-web. Customer dapat akses dashboard mereka, bukan source code installasi sendiri. Itu beda dengan "open source self-hosted" — kami SaaS hosted.

**Q: Kalau ada bug, gimana?**
A: Report ke Kamil via WhatsApp. Kamil fix ASAP (biasanya 1-24 jam). Lu (Alvin) jangan janjiin timeline ke customer, bilang "saya cek dulu sama tim teknis, balik dalam 1×24 jam".

---

## 15. Contact

**Kamil Alfaris** — Founder
- WhatsApp: +62 812-9398-8757
- Email: kamilalfaris@gmail.com
- LinkedIn: linkedin.com/in/kamil-alfaris
- GitHub: github.com/AlvaricVon

---

*Document version: 1.0 · Updated: May 2026*
