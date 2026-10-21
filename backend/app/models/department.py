import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, DateTime
from sqlalchemy.orm import relationship
from app.core.database import Base

class Department(Base):
    __tablename__ = "departments"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    code = Column(String(20), unique=True, index=True, nullable=False)   # e.g., "CSE", "CSBS", "AIML", "IT"
    name = Column(String(255), nullable=False)                          # e.g., "Computer Science & Engineering"
    description = Column(String(500), nullable=True)

    users = relationship("User", back_populates="department")
    students = relationship("Student", back_populates="department")
    
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
