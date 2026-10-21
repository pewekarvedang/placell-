import enum
import uuid
from datetime import datetime, timezone, date
from sqlalchemy import Column, String, Float, Integer, DateTime, Date, Enum, ForeignKey, Text
from sqlalchemy.orm import relationship
from app.core.database import Base

class DriveStatus(str, enum.Enum):
    UPCOMING = "UPCOMING"
    ACTIVE = "ACTIVE"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"

class ApplicationStatus(str, enum.Enum):
    APPLIED = "APPLIED"
    SHORTLISTED = "SHORTLISTED"
    INTERVIEWED = "INTERVIEWED"
    SELECTED = "SELECTED"
    REJECTED = "REJECTED"

class PlacementDrive(Base):
    __tablename__ = "placement_drives"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    company_id = Column(String(36), ForeignKey("companies.id", ondelete="CASCADE"), nullable=False)
    job_role_id = Column(String(36), ForeignKey("job_roles.id", ondelete="CASCADE"), nullable=False)
    
    title = Column(String(255), nullable=False)
    drive_date = Column(Date, default=date.today, nullable=False)
    status = Column(Enum(DriveStatus), default=DriveStatus.UPCOMING, nullable=False)
    eligibility_cgpa = Column(Float, default=6.5, nullable=False)
    eligibility_criteria = Column(Text, nullable=True)
    ctc_offered_lpa = Column(Float, nullable=False, default=6.0)
    rounds_description = Column(Text, nullable=True)

    company = relationship("Company", back_populates="placement_drives")
    job_role = relationship("JobRole", back_populates="placement_drives")
    applications = relationship("Application", back_populates="placement_drive", cascade="all, delete-orphan")
    experiences = relationship("PlacementExperience", back_populates="placement_drive")

    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)

class Application(Base):
    __tablename__ = "applications"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    placement_drive_id = Column(String(36), ForeignKey("placement_drives.id", ondelete="CASCADE"), nullable=False)
    student_id = Column(String(36), ForeignKey("students.id", ondelete="CASCADE"), nullable=False)
    status = Column(Enum(ApplicationStatus), default=ApplicationStatus.APPLIED, nullable=False)

    placement_drive = relationship("PlacementDrive", back_populates="applications")
    student = relationship("Student", back_populates="applications")

    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
