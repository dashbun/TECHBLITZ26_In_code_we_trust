from typing import List, Dict
from datetime import datetime, timedelta
from src.database.supabase_client import SupabaseClient

class SequenceEngine:
    def __init__(self):
        self.db = SupabaseClient()
        self.sequences = {
            "cold_outreach": [
                {"day": 0, "action": "initial_message"},
                {"day": 2, "action": "follow_up_1"},
                {"day": 5, "action": "follow_up_2"},
                {"day": 10, "action": "breakup"}
            ]
        }

    def assign_sequence(self, lead_id: str, sequence_type: str = "cold_outreach"):
        """Start sequence for lead."""
        seq = self.sequences.get(sequence_type, [])
        for step in seq:
            # Schedule via cron/webhook/DB trigger (placeholder)
            print(f"Schedule {step['action']} for lead {lead_id} on day {step['day']}")

    def check_next_step(self, lead_id: str) -> Dict:
        """Check if next sequence step due."""
        lead = self.db.get_lead_by_id(lead_id)  # Assume method exists
        # Logic to compute next step
        return {"due": False, "action": None}
