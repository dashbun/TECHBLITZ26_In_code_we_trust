import requests
import os
from dotenv import load_dotenv
from typing import Dict, Any

load_dotenv()

class Enricher:
    def __init__(self):
        self.api_key = os.getenv("APOLLO_IO_KEY")
        self.base_url = "https://api.apollo.io/v1"

    def enrich_person(self, email: str) -> Dict[str, Any]:
        """Enrich person via Apollo.io."""
        if not self.api_key:
            return {"error": "APOLLO_IO_KEY not set"}
        
        headers = {"Cache-Control": "no-cache", "X-Api-Key": self.api_key}
        params = {"email": email}
        
        response = requests.get(
            f"{self.base_url}/people/match",
            headers=headers,
            params=params
        )
        
        if response.status_code == 200:
            return response.json()["person"]
        return {"error": "Enrichment failed"}

    def enrich_company(self, domain: str) -> Dict[str, Any]:
        """Enrich company."""
        headers = {"X-Api-Key": self.api_key}
        response = requests.get(
            f"{self.base_url}/organizations/find",
            headers=headers,
            params={"domain": domain}
        )
        return response.json().get("organization", {}) if response.status_code == 200 else {}
