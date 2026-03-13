from typing import Dict, Any
from src.utils.helpers import validate_email, validate_phone
from src.database.models import Lead

class LeadScorer:
    def __init__(self):
        self.weights = {
            "email_valid": 0.2,
            "phone_valid": 0.2,
            "company_size": 0.3,
            "industry": 0.2,
            "ml_score": 0.1  # Placeholder for ML
        }

    def score_lead(self, lead: Dict[str, Any]) -> int:
        """Hybrid scoring: rules + ML placeholder."""
        score = 0
        
        # Rule-based
        if validate_email(lead.get("email", "")):
            score += 20
        if validate_phone(lead.get("phone", "")):
            score += 20
        
        # Company size placeholder
        company = lead.get("company", "").lower()
        if any(kw in company for kw in ["inc", "corp", "llc"]):
            score += 30
        elif any(kw in company for kw in ["tech", "software"]):
            score += 40
        
        # Industry boost
        if "saas" in company or "enterprise" in company:
            score += 20
        
        # ML placeholder (replace with real model)
        ml_score = hash(lead.get("email", "")) % 100  # Dummy
        score += int(ml_score * 0.1)
        
        return min(score, 100)
