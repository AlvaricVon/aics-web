# AICS Web

Landing page untuk AICS (AI Customer Support). Static HTML + Supabase backend.

## Backend
- Supabase project: `stcywvcnbbapshrzqblk` (region ap-southeast-1)
- URL: https://stcywvcnbbapshrzqblk.supabase.co
- Edge function: `cs-demo` (publik, JWT-less, untuk live demo widget)
- Tables: `leads`, `audit_requests`, `demo_chats`, `outreach`

## Cara update content
Edit `index.html`. Deploy ulang dengan `vercel deploy --prod` atau via MCP.

## Cara lihat leads
1. Login ke Supabase: https://supabase.com/dashboard/project/stcywvcnbbapshrzqblk
2. Buka Table Editor → `audit_requests` atau `leads`
