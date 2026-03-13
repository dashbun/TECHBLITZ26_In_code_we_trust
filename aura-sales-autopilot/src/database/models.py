from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class LeadBase(BaseModel):
    name: str
    email: str
    phone: Optional[str] = None
    company: Optional[str] = None

class LeadCreate(LeadBase):
    pass

class Lead(LeadBase):
    id: str
    score: int
    status: str
    rep_id: Optional[str] = None
    source: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class RepBase(BaseModel):
    telegram_id: Optional[int] = None
    whatsapp_id: Optional[str] = None
    name: str

class RepCreate(RepBase):
    pass

class Rep(RepBase):
    id: str
    active: bool
    created_at: datetime

    class Config:
        from_attributes = True
