import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, Float, DateTime, ForeignKey, Text, JSON
from sqlalchemy.orm import relationship
from app.core.database import Base

class NLPAnalysisResult(Base):
    __tablename__ = "nlp_analysis_results"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    experience_id = Column(String(36), ForeignKey("placement_experiences.id", ondelete="CASCADE"), unique=True, nullable=False)
    
    sentiment_label = Column(String(20), nullable=False)               # "POSITIVE", "NEUTRAL", "NEGATIVE"
    sentiment_score = Column(Float, nullable=False)                    # e.g., 0.85
    sentiment_confidence = Column(Float, nullable=False, default=0.90) # e.g., 0.92
    
    inferred_difficulty = Column(String(20), nullable=False, default="MODERATE") # "EASY", "MODERATE", "HARD"
    extracted_skills = Column(JSON, nullable=False, default=list)      # ["Python", "SQL", "DBMS", "REST APIs"]
    extracted_topics = Column(JSON, nullable=False, default=list)      # ["Coding", "System Design", "Database Queries"]
    frequently_mentioned_terms = Column(JSON, nullable=False, default=list)

    experience = relationship("PlacementExperience", back_populates="nlp_result")

    processed_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)

class ReadinessEvaluation(Base):
    __tablename__ = "readiness_evaluations"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    student_id = Column(String(36), ForeignKey("students.id", ondelete="CASCADE"), nullable=False)
    
    readiness_percentage = Column(Float, nullable=False)               # 0.0 to 100.0 %
    readiness_tier = Column(String(50), nullable=False)                # "NEEDS_IMPROVEMENT", "DEVELOPING", "PLACEMENT_READY", "STRONG"
    feature_breakdown = Column(JSON, nullable=False, default=dict)     # Academic, Skills, Projects, Experience contributions
    
    evaluated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)

    student = relationship("Student", back_populates="readiness_evaluations")

class Recommendation(Base):
    __tablename__ = "recommendations"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    student_id = Column(String(36), ForeignKey("students.id", ondelete="CASCADE"), nullable=False)
    target_role_id = Column(String(36), ForeignKey("job_roles.id", ondelete="SET NULL"), nullable=True)
    
    skill_name = Column(String(100), nullable=False)
    priority = Column(String(20), default="HIGH", nullable=False)      # "HIGH", "MEDIUM", "LOW"
    rationale_text = Column(Text, nullable=False)                      # Statistical explainable justification
    actionable_steps = Column(JSON, nullable=True, default=list)
    
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)

    student = relationship("Student", back_populates="recommendations")
