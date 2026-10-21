import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, Float, Integer, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from app.core.database import Base

class Student(Base):
    __tablename__ = "students"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False)
    roll_number = Column(String(50), unique=True, index=True, nullable=False)
    department_id = Column(String(36), ForeignKey("departments.id", ondelete="RESTRICT"), nullable=False)
    
    # Academic & Professional attributes (Zero sensitive demographic traits)
    cgpa = Column(Float, nullable=False, default=7.0)
    graduation_year = Column(Integer, nullable=False, default=2026)
    projects_count = Column(Integer, nullable=False, default=2)
    internships_count = Column(Integer, nullable=False, default=0)
    certifications_count = Column(Integer, nullable=False, default=1)
    
    preferred_role_title = Column(String(255), default="Software Engineer", nullable=False)
    bio = Column(Text, nullable=True)
    resume_url = Column(String(500), nullable=True)

    # Relationships
    user = relationship("User", back_populates="student_profile")
    department = relationship("Department", back_populates="students")
    skills = relationship("StudentSkill", back_populates="student", cascade="all, delete-orphan")
    applications = relationship("Application", back_populates="student", cascade="all, delete-orphan")
    experiences = relationship("PlacementExperience", back_populates="student", cascade="all, delete-orphan")
    readiness_evaluations = relationship("ReadinessEvaluation", back_populates="student", cascade="all, delete-orphan")
    recommendations = relationship("Recommendation", back_populates="student", cascade="all, delete-orphan")

    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)

class StudentSkill(Base):
    __tablename__ = "student_skills"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    student_id = Column(String(36), ForeignKey("students.id", ondelete="CASCADE"), nullable=False)
    skill_id = Column(String(36), ForeignKey("skills.id", ondelete="CASCADE"), nullable=False)
    proficiency_level = Column(String(20), default="Intermediate", nullable=False) # "Beginner", "Intermediate", "Advanced"

    student = relationship("Student", back_populates="skills")
    skill = relationship("Skill", back_populates="student_skills")
