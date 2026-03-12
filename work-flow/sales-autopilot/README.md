# SalesAutopilot

## Setup

1. Person A runs `supabase/migrations/001_init.sql` in Supabase SQL editor
2. Copy `.env.example` to `.env` and fill in all values
3. Share `.env` with team securely (never commit it)
4. Each person runs their service:

```
python services/person_X/main.py
```

## Services

Person A — Webhook, scoring, queue worker (port 8000)

Person B — Telegram bot, approval flow

Person C — Sequence engine, WhatsApp + Email outreach

## Demo

```
python demo/seed_lead.py
python demo/test_dedup.py
```
