import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, Float, DateTime, ForeignKey, Text, Integer
from sqlalchemy.orm import relationship
from app.core.database import Base

class Company(Base):
    __tablename__ = "companies"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(255), unique=True, index=True, nullable=False)
    industry = Column(String(100), nullable=False)                         # e.g., "Information Technology", "FinTech", "Consulting"
    company_type = Column(String(50), nullable=False, default="Product")   # "Product", "Service", "Startup"
    website = Column(String(255), nullable=True)
    location = Column(String(255), nullable=True)
    ctc_min_lpa = Column(Float, nullable=False, default=4.0)
    ctc_max_lpa = Column(Float, nullable=False, default=12.0)
    description = Column(Text, nullable=True)

    job_roles = relationship("JobRole", back_populates="company", cascade="all, delete-orphan")
    placement_drives = relationship("PlacementDrive", back_populates="company", cascade="all, delete-orphan")
    experiences = relationship("PlacementExperience", back_populates="company")

    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)

class JobRole(Base):
    __tablename__ = "job_roles"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    company_id = Column(String(36), ForeignKey("companies.id", ondelete="CASCADE"), nullable=False)
    title = Column(String(255), index=True, nullable=False)                # e.g., "Full Stack Developer", "Data Analyst"
    min_cgpa = Column(Float, nullable=False, default=6.5)
    description = Column(Text, nullable=True)

    company = relationship("Company", back_populates="job_roles")
    skills = relationship("JobRoleSkill", back_populates="job_role", cascade="all, delete-orphan")
    placement_drives = relationship("PlacementDrive", back_populates="job_role")
    experiences = relationship("PlacementExperience", back_populates="job_role")

    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)

class JobRoleSkill(Base):
    __tablename__ = "job_role_skills"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    job_role_id = Column(String(36), ForeignKey("job_roles.id", ondelete="CASCADE"), nullable=False)
    skill_id = Column(String(36), ForeignKey("skills.id", ondelete="CASCADE"), nullable=False)
    importance_weight = Column(Float, default=1.0, nullable=False)        # 1.0 = Normal, 2.0 = Crucial

    job_role = relationship("JobRole", back_populates="skills")
    skill = relationship("Skill", back_populates="job_role_skills")
