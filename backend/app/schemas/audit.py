from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict

class AuditLogResponse(BaseModel):
    id: str
    user_id: Optional[str] = None
    user_email: Optional[str] = None
    user_role: Optional[str] = None
    action: str
    entity_name: str
    entity_id: Optional[str] = None
    details: Optional[str] = None
    ip_address: Optional[str] = None
    timestamp: datetime
    model_config = ConfigDict(from_attributes=True)
