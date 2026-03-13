from typing import Dict
from datetime import datetime
from src.database.supabase_client import SupabaseClient, supabase
from src.utils.logger import log


class SequenceEngine:
    def __init__(self):
        self.db = SupabaseClient()
        self.sequences = {
            "cold_outreach": [
                {"day": 0, "action": "initial_message"},
                {"day": 2, "action": "follow_up_1"},
                {"day": 5, "action": "follow_up_2"},
                {"day": 10, "action": "breakup"},
            ]
        }

    def assign_sequence(self, lead_id: str, sequence_type: str = "cold_outreach"):
        """Kick off the sequence for a lead via the DB atomic function."""
        try:
            result = supabase.rpc(
                "start_sequence_if_not_started", {"p_lead_id": lead_id}
            ).execute()
            if result.data:
                log("ok", "sequence_started", lead_id=lead_id[:8], type=sequence_type)
            else:
                log("warn", "sequence_already_started", lead_id=lead_id[:8])
        except Exception as exc:
            log("error", "sequence_start_failed", lead_id=lead_id[:8], error=str(exc))

    def check_next_step(self, lead_id: str) -> Dict:
        """Check if next sequence step is due for a given lead."""
        lead = self.db.get_lead_by_id(lead_id)
        if not lead:
            return {"due": False, "action": None}
        last_contacted = lead.get("last_contacted")
        step = lead.get("sequence_step", 0)
        seq = self.sequences.get("cold_outreach", [])
        if step >= len(seq):
            return {"due": False, "action": None}
        if last_contacted is None:
            return {"due": True, "action": seq[step]["action"]}
        last_dt = datetime.fromisoformat(last_contacted.replace("Z", "+00:00"))
        days_needed = seq[step]["day"]
        days_passed = (datetime.utcnow() - last_dt).days
        return {
            "due": days_passed >= days_needed,
            "action": seq[step]["action"] if days_passed >= days_needed else None,
        }

    def check_due_steps(self):
        """Called by APScheduler every hour — process all in-sequence leads."""
        leads = self.db.get_leads(status="in_sequence")
        for lead in leads:
            result = self.check_next_step(lead["id"])
            if result["due"]:
                log("info", "sequence_step_due", lead_id=lead["id"][:8], action=result["action"])
                # TODO: dispatch message via bot


# Module-level async helper used by telegram_rep.py
async def start_sequence(lead_id: str) -> None:
    """Async wrapper to kick off the sequence (safe to call from asyncio tasks)."""
    engine = SequenceEngine()
    engine.assign_sequence(lead_id)
