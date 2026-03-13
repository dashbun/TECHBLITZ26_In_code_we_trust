import os
from dotenv import load_dotenv
from supabase import create_client, Client
from typing import Optional

load_dotenv()

class SupabaseClient:
    def __init__(self):
        self.url: str = os.getenv("SUPABASE_URL", "")
        self.key: str = os.getenv("SUPABASE_KEY", "")
        self.client: Client = create_client(self.url, self.key)

    # --- Leads ---

    def get_leads(self, status: Optional[str] = None) -> list:
        """Fetch leads filtered by status."""
        query = self.client.table("leads").select("*")
        if status:
            query = query.eq("status", status)
        response = query.execute()
        return response.data or []

    def get_lead_by_id(self, lead_id: str) -> Optional[dict]:
        """Fetch a single lead by UUID."""
        response = self.client.table("leads").select("*").eq("id", lead_id).single().execute()
        return response.data

    def create_lead(self, lead_data: dict) -> dict:
        """Insert new lead."""
        response = self.client.table("leads").insert(lead_data).execute()
        return response.data[0] if response.data else {}

    def transition_lead(self, lead_id: str, new_status: str, actor: str) -> bool:
        """Call the atomic transition_lead Postgres function."""
        response = self.client.rpc(
            "transition_lead",
            {"p_lead_id": lead_id, "p_new_status": new_status, "p_actor": actor},
        ).execute()
        return bool(response.data)

    def get_state_transitions(self, since_iso: str) -> list:
        """Fetch state transitions since a given ISO timestamp."""
        response = (
            self.client.table("state_transitions")
            .select("*")
            .gte("created_at", since_iso)
            .execute()
        )
        return response.data or []

    # --- Reps ---

    def get_reps(self) -> list:
        """Fetch active reps."""
        response = self.client.table("reps").select("*").eq("active", True).execute()
        return response.data or []


# Module-level singleton — imported by bots as `from src.database.supabase_client import supabase`
_client = SupabaseClient()
supabase = _client.client
