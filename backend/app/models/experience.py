import enum
import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, Integer, Float, DateTime, Enum, ForeignKey, Text, Boolean
from sqlalchemy.orm import relationship
from app.core.database import Base

class ExperienceStatus(str, enum.Enum):
    PENDING = "PENDING"
    VERIFIED = "VERIFIED"
    REJECTED = "REJECTED"

class RoundType(str, enum.Enum):
    APTITUDE = "APTITUDE"
    CODING = "CODING"
    TECHNICAL_INTERVIEW = "TECHNICAL_INTERVIEW"
    HR_INTERVIEW = "HR_INTERVIEW"
    GROUP_DISCUSSION = "GROUP_DISCUSSION"
    SYSTEM_DESIGN = "SYSTEM_DESIGN"
    OTHER = "OTHER"

class PlacementExperience(Base):
    __tablename__ = "placement_experiences"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    student_id = Column(String(36), ForeignKey("students.id", ondelete="CASCADE"), nullable=False)
    placement_drive_id = Column(String(36), ForeignKey("placement_drives.id", ondelete="SET NULL"), nullable=True)
    company_id = Column(String(36), ForeignKey("companies.id", ondelete="CASCADE"), nullable=False)
    job_role_id = Column(String(36), ForeignKey("job_roles.id", ondelete="SET NULL"), nullable=True)
    
    overall_rating = Column(Integer, default=4, nullable=False)        # 1 - 5 stars
    difficulty_rating = Column(Integer, default=3, nullable=False)     # 1 - 5 stars
    rounds_count = Column(Integer, default=3, nullable=False)
    questions_asked = Column(Text, nullable=True)
    skills_tested = Column(String(500), nullable=True)                 # Comma-separated or tagged
    free_text_feedback = Column(Text, nullable=False)
    is_placed = Column(Boolean, default=False, nullable=False)
    
    # Moderation & Verification (Enterprise workflow)
    status = Column(Enum(ExperienceStatus), default=ExperienceStatus.VERIFIED, nullable=False)
    verified_by_user_id = Column(String(36), ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    moderation_notes = Column(Text, nullable=True)

    # Relationships
    student = relationship("Student", back_populates="experiences")
    placement_drive = relationship("PlacementDrive", back_populates="experiences")
    company = relationship("Company", back_populates="experiences")
    job_role = relationship("JobRole", back_populates="experiences")
    rounds = relationship("InterviewRound", back_populates="experience", cascade="all, delete-orphan")
    nlp_result = relationship("NLPAnalysisResult", back_populates="experience", uselist=False, cascade="all, delete-orphan")

    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)

class InterviewRound(Base):
    __tablename__ = "interview_rounds"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    experience_id = Column(String(36), ForeignKey("placement_experiences.id", ondelete="CASCADE"), nullable=False)
    round_number = Column(Integer, nullable=False)
    round_type = Column(Enum(RoundType), nullable=False, default=RoundType.TECHNICAL_INTERVIEW)
    round_title = Column(String(100), nullable=True)
    description = Column(Text, nullable=True)
    duration_minutes = Column(Integer, default=45, nullable=True)
    difficulty = Column(Integer, default=3, nullable=True)             # 1 - 5

    experience = relationship("PlacementExperience", back_populates="rounds")
