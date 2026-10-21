import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from app.core.database import Base

class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(36), ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    action = Column(String(100), nullable=False)                         # e.g., "LOGIN", "SUBMIT_EXPERIENCE", "VERIFY_EXPERIENCE", "CREATE_DRIVE"
    entity_name = Column(String(50), nullable=False)                     # e.g., "PlacementExperience", "User", "PlacementDrive"
    entity_id = Column(String(36), nullable=True)
    details = Column(Text, nullable=True)
    ip_address = Column(String(45), nullable=True)
    
    user = relationship("User", back_populates="audit_logs")

    timestamp = Column(DateTime, default=lambda: datetime.now(timezone.utc), index=True, nullable=False)
