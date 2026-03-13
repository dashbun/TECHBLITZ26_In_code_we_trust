import os
from dotenv import load_dotenv
from supabase import create_client, Client
from typing import Optional

load_dotenv()

class SupabaseClient:
    def __init__(self):
        self.url: str = os.getenv("SUPABASE_URL")
        self.key: str = os.getenv("SUPABASE_KEY")
        self.client: Client = create_client(self.url, self.key)

    def get_leads(self, status: Optional[str] = None) -> list:
        """Fetch leads filtered by status."""
        query = self.client.table("leads").select("*")
        if status:
            query = query.eq("status", status)
        data, count = query.execute()
        return data

    def create_lead(self, lead_data: dict) -> dict:
        """Insert new lead."""
        data, count = self.client.table("leads").insert(lead_data).execute()
        return data[0]

    def get_reps(self) -> list:
        """Fetch active reps."""
        data, count = self.client.table("reps").select("*").eq("active", True).execute()
        return data
