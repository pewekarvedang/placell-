from typing import Optional
from sqlalchemy.orm import Session
from app.models.audit_log import AuditLog

def log_action(
    db: Session,
    action: str,
    entity_name: str,
    user_id: Optional[str] = None,
    entity_id: Optional[str] = None,
    details: Optional[str] = None,
    ip_address: Optional[str] = None
) -> AuditLog:
    """Creates an immutable audit log entry."""
    entry = AuditLog(
        user_id=user_id,
        action=action,
        entity_name=entity_name,
        entity_id=entity_id,
        details=details,
        ip_address=ip_address
    )
    db.add(entry)
    db.commit()
    return entry
