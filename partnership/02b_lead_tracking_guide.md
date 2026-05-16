# Lead Tracking — Setup Guide

## Cara Setup Google Sheet

1. Buka https://sheets.google.com → Blank spreadsheet
2. File → **Import** → tab "Upload" → drag file `02_lead_tracking_template.csv`
3. Import location: **Replace current sheet**
4. Separator type: **Comma**
5. Klik Import data

Atau lebih cepat:
1. Buka https://sheets.new
2. Copy paste konten file CSV langsung
3. Highlight kolom A → **Data → Split text to columns** → comma

---

## Penjelasan Tiap Kolom

| Kolom | Tipe | Cara Isi |
|---|---|---|
| **Tanggal Outreach** | Date (YYYY-MM-DD) | Tanggal lu kirim DM/email/WA |
| **Nama Prospect** | Text | Nama orang yang dihubungi |
| **Channel** | Dropdown: LinkedIn / WhatsApp / Email / Instagram DM / Komunitas | Platform tempat lu outreach |
| **Link Profile** | URL | Link LinkedIn / IG / WA mereka |
| **Perusahaan** | Text | Nama bisnis/perusahaan mereka |
| **Industri** | Dropdown: E-commerce / SaaS / F&B / Edu / Beauty / Retail / Other | Industri prospect |
| **Posisi** | Text | Founder / Owner / Head of CX / Marketing Manager / dll |
| **Pesan Dikirim (Singkat)** | Text (max 100 char) | Ringkasan DM lu (1 kalimat) |
| **Status** | Dropdown (lihat di bawah) | Update tiap progress |
| **Tanggal Reply** | Date | Kapan mereka balas (kalau ada) |
| **Next Action** | Text | What lu harus do next + kapan |
| **Hari Trial** | Number | Hari ke-berapa trial mereka (1-14) |
| **Tanggal Bayar** | Date | Kapan mereka transfer |
| **Plan Dipilih** | Dropdown: Lite / Pro / Business / Custom | Plan yang mereka beli |
| **Komisi (Rp)** | Number | Komisi Alvin per bulan (kalau dia bawa) |
| **Notes** | Long text | Catatan apapun yang penting |

### Status Lifecycle (urut dari awal ke closing):

1. **Sent** — DM/WA/email udah dikirim
2. **Opened** — mereka udah baca (kalau LinkedIn read receipt on, WA centang biru, email open tracked)
3. **Replied** — mereka balas chat
4. **In Discussion** — udah ngobrol panjang, ada interest
5. **Demo Booked** — udah jadwalin Zoom/Meet
6. **Demo Done** — demo selesai, waiting decision
7. **Trial Signup** — mereka udah daftar trial 14 hari
8. **Paid** — sudah convert ke paying customer
9. **Lost** — tidak jadi (write reason di Notes)

### Conditional Formatting (Recommended)

Pakai Google Sheets conditional formatting biar visual:
- Status "Paid" → background hijau
- Status "Lost" → background merah
- Status "Demo Booked" / "Trial Signup" → background kuning
- Next Action contains "Follow up" + tanggal past today → background orange

Tutorial: Format → Conditional formatting → Custom formula → `=$I2="Paid"` → fill green

---

## Cara Pakai Daily

### Pagi (5 menit)
1. Buka sheet
2. Filter "Next Action" → cari tanggal hari ini
3. Eksekusi action satu per satu, update status
4. Tambahkan row baru kalau ada outreach baru

### Akhir Bulan (15 menit)
1. Hitung:
   - Total DM sent bulan ini
   - Total reply (= konversi rate)
   - Total trial signup
   - Total paying customer
2. Update KPI di docs
3. Identify pattern: pesan template mana yang paling banyak dapat reply

---

## Pivot Table (Optional, untuk analisis)

Klik Insert → Pivot table → pakai kolom:
- Rows: Channel + Status
- Values: COUNTA of Nama Prospect

Ini kasih lu breakdown:
- Berapa % dari LinkedIn DM yang convert ke Paid?
- Channel mana yang paling efektif?
- Industri mana yang paling responsive?
