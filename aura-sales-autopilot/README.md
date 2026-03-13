# Aura Sales Autopilot

A FastAPI-based sales automation system with Telegram/WhatsApp bots for users/reps, Supabase DB, lead scoring, enrichment, and sequences.

## Setup
1. Copy `.env.example` to `.env` and fill values.
2. `pip install -r requirements.txt`
3. Apply `migrations/schema.sql` to Supabase.
4. `uvicorn src.main:app --reload`

## Structure
- `src/main.py`: FastAPI entrypoint
- `src/database/`: Supabase client & models
- `src/bots/`: User & Rep Telegram/WhatsApp bots
- `src/agents/`: Lead scorer, enricher, sequence engine
- `src/knowledge/`: Product KB & vector search
- `src/utils/`: Helpers & logger

## Bots
- User bots: Handle lead intake
- Rep bots: Assign & track leads
