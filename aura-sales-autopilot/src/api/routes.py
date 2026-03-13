"""
REST API routes for the Aura Sales Autopilot — consumed by the frontend dashboard.

All endpoints are mounted under /api via main.py.
"""

from datetime import datetime, timedelta
from typing import Optional

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel

from src.database.supabase_client import SupabaseClient

router = APIRouter(prefix="/api", tags=["dashboard"])
db = SupabaseClient()


# ---------------------------------------------------------------------------
# Response helpers — map DB snake_case → frontend camelCase shape
# ---------------------------------------------------------------------------

def _db_lead_to_frontend(lead: dict) -> dict:
    """
    Convert a Supabase leads row into the shape expected by the React frontend:
      Lead { id, name, company, source, score, intent, status,
             receivedAt, lastActivity?, aiSummary, aiRationale,
             lot_size?, est_profit?, icp_fit? }
    """
    score = lead.get("score") or 0
    if score >= 70:
        intent = "Hot"
    elif score >= 40:
        intent = "Warm"
    else:
        intent = "Cold"

    # Map backend status values → frontend display statuses
    status_map = {
        "queued": "New Lead",
        "scoring": "New Lead",
        "pending_approval": "New Lead",
        "approved": "Contacted",
        "in_sequence": "Interested",
        "converted": "Closed",
        "rejected": "Closed",
        "snoozed": "Contacted",
        "dead": "Closed",
    }
    raw_status = lead.get("status", "queued")
    frontend_status = status_map.get(raw_status, "New Lead")

    # Derive a simple AI summary from available fields
    company = lead.get("company") or "Unknown Company"
    industry = lead.get("industry") or ""
    preferred = lead.get("preferred_categories") or []
    ai_summary = (
        f"{lead['name']} from {company}"
        + (f" ({industry})" if industry else "")
        + (f" — interested in {', '.join(preferred[:2])}" if preferred else "")
        + "."
    )
    ai_rationale = (
        f"ICP fit: {lead.get('icp_fit', 'unknown')}. "
        f"Purchase intent score: {lead.get('purchase_intent', 0)}/40. "
        f"Estimated profit: ₹{lead.get('est_profit', 0)}."
    )

    # Last activity from conversation history
    history = lead.get("conversation_history") or []
    last_activity = None
    if history:
        last_msg = history[-1]
        last_activity = last_msg.get("msg") or last_msg.get("message")

    return {
        "id": lead["id"],
        "name": lead.get("name", "Unknown"),
        "company": company,
        "source": _map_source(lead.get("source", "website_form")),
        "score": score,
        "intent": intent,
        "status": frontend_status,
        "backendStatus": raw_status,          # raw value for PATCH endpoint
        "receivedAt": lead.get("created_at", datetime.utcnow().isoformat()),
        "lastActivity": last_activity,
        "aiSummary": ai_summary,
        "aiRationale": ai_rationale,
        "lot_size": lead.get("lot_size"),
        "est_profit": lead.get("est_profit"),
        "icp_fit": lead.get("icp_fit"),
    }


def _map_source(raw: str) -> str:
    return {
        "telegram_user": "WhatsApp",   # closest match in frontend enum
        "whatsapp_user": "WhatsApp",
        "website_form": "Website",
        "instagram": "Instagram",
    }.get(raw, "Website")


# ---------------------------------------------------------------------------
# Request bodies
# ---------------------------------------------------------------------------

class StatusUpdate(BaseModel):
    status: str      # backend status value e.g. "approved", "rejected"
    actor: str = "dashboard"


# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------

@router.get("/leads")
def get_leads(status: Optional[str] = Query(default=None)):
    """Return all leads, optionally filtered by backend status."""
    rows = db.get_leads(status=status)
    return [_db_lead_to_frontend(r) for r in rows]


@router.get("/leads/{lead_id}")
def get_lead(lead_id: str):
    """Return a single lead by UUID."""
    row = db.get_lead_by_id(lead_id)
    if not row:
        raise HTTPException(status_code=404, detail="Lead not found")
    return _db_lead_to_frontend(row)


@router.patch("/leads/{lead_id}/status")
def update_lead_status(lead_id: str, body: StatusUpdate):
    """Transition a lead's status using the atomic Postgres function."""
    success = db.transition_lead(lead_id, body.status, body.actor)
    if not success:
        raise HTTPException(
            status_code=409,
            detail="Transition not allowed (invalid state or already processed)",
        )
    return {"success": True}


@router.post("/leads/{lead_id}/approve-outreach")
async def approve_outreach(lead_id: str):
    """
    Approve outreach for a lead:
      1. Transition to 'approved'
      2. Start the outreach sequence
    """
    from src.agents.sequence_engine import start_sequence

    # Transition pending_approval → approved
    approved = db.transition_lead(lead_id, "approved", "dashboard")
    if not approved:
        raise HTTPException(
            status_code=409,
            detail="Could not approve — lead may already be processed",
        )

    # Kick off sequence (non-blocking)
    await start_sequence(lead_id)

    return {"success": True, "message": "Outreach approved — sequence started"}


@router.get("/dashboard/metrics")
def get_dashboard_metrics():
    """
    Compute real-time dashboard metrics from the leads and state_transitions tables.
    """
    today_iso = datetime.utcnow().date().isoformat()

    # All leads created today
    all_leads = db.get_leads()
    leads_today = [
        l for l in all_leads
        if l.get("created_at", "").startswith(today_iso)
    ]

    hot_leads = sum(1 for l in all_leads if (l.get("score") or 0) >= 70)

    follow_ups_pending = sum(
        1 for l in all_leads
        if l.get("status") in ("pending_approval", "approved")
    )

    # Meetings scheduled — proxy: in_sequence leads with lot_size > 1
    meetings_scheduled = sum(
        1 for l in all_leads
        if l.get("status") == "in_sequence" and (l.get("lot_size") or 0) > 1
    )

    # Deals closed today
    transitions = db.get_state_transitions(since_iso=today_iso + "T00:00:00")
    deals_closed = sum(1 for t in transitions if t.get("to_state") == "converted")

    return {
        "leadsToday": len(leads_today),
        "hotLeads": hot_leads,
        "followUpsPending": follow_ups_pending,
        "meetingsScheduled": meetings_scheduled,
        "dealsClosed": deals_closed,
    }


@router.get("/outreach/drafts")
def get_outreach_drafts():
    """
    Return leads pending approval as 'outreach drafts' for the Outreach page.
    Each draft contains a generated message preview.
    """
    pending = db.get_leads(status="pending_approval")
    drafts = []
    for lead in pending:
        name = lead.get("name", "there")
        company = lead.get("company") or "your company"
        preferred = lead.get("preferred_categories") or []
        category_str = preferred[0] if preferred else "our products"

        drafts.append({
            "id": f"draft_{lead['id'][:8]}",
            "leadId": lead["id"],
            "type": "WhatsApp",
            "content": (
                f"Hey {name}! 👋 Thanks for your interest in {category_str}. "
                f"I'd love to help you find the perfect option for {company}. "
                f"Would you like me to share some tailored recommendations? 😊"
            ),
            "status": "Draft",
        })
    return drafts
