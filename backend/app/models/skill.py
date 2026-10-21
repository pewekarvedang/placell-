import enum
import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, DateTime, Enum
from sqlalchemy.orm import relationship
from app.core.database import Base

class SkillCategory(str, enum.Enum):
    PROGRAMMING = "PROGRAMMING"
    DATABASE = "DATABASE"
    CLOUD_DEVOPS = "CLOUD_DEVOPS"
    CORE_CS = "CORE_CS"
    FRAMEWORK = "FRAMEWORK"
    AI_ML = "AI_ML"
    SOFT_SKILL = "SOFT_SKILL"

class Skill(Base):
    __tablename__ = "skills"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(100), unique=True, index=True, nullable=False)
    category = Column(Enum(SkillCategory), nullable=False, default=SkillCategory.PROGRAMMING)
    description = Column(String(255), nullable=True)

    student_skills = relationship("StudentSkill", back_populates="skill", cascade="all, delete-orphan")
    job_role_skills = relationship("JobRoleSkill", back_populates="skill", cascade="all, delete-orphan")
    
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
