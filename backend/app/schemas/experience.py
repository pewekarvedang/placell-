from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field, ConfigDict
from app.models.experience import ExperienceStatus, RoundType

class RoundCreate(BaseModel):
    round_number: int
    round_type: RoundType
    round_title: Optional[str] = None
    description: Optional[str] = None
    duration_minutes: Optional[int] = 45
    difficulty: int = Field(3, ge=1, le=5)

class RoundResponse(RoundCreate):
    id: str
    model_config = ConfigDict(from_attributes=True)

class ExperienceCreate(BaseModel):
    company_id: str
    job_role_id: Optional[str] = None
    placement_drive_id: Optional[str] = None
    overall_rating: int = Field(4, ge=1, le=5)
    difficulty_rating: int = Field(3, ge=1, le=5)
    rounds_count: int = Field(3, ge=1, le=10)
    questions_asked: Optional[str] = None
    skills_tested: Optional[str] = None
    free_text_feedback: str
    is_placed: bool = False
    rounds: List[RoundCreate] = []

class NLPResultResponse(BaseModel):
    sentiment_label: str
    sentiment_score: float
    sentiment_confidence: float
    inferred_difficulty: str
    extracted_skills: List[str]
    extracted_topics: List[str]
    frequently_mentioned_terms: List[str]
    model_config = ConfigDict(from_attributes=True)

class ExperienceResponse(BaseModel):
    id: str
    student_id: str
    student_roll_number: str
    student_department: str
    company_id: str
    company_name: str
    job_role_id: Optional[str] = None
    job_role_title: Optional[str] = None
    overall_rating: int
    difficulty_rating: int
    rounds_count: int
    questions_asked: Optional[str] = None
    skills_tested: Optional[str] = None
    free_text_feedback: str
    is_placed: bool
    status: ExperienceStatus
    created_at: datetime
    rounds: List[RoundResponse] = []
    nlp_result: Optional[NLPResultResponse] = None
    model_config = ConfigDict(from_attributes=True)

class ExperienceModeration(BaseModel):
    status: ExperienceStatus
    moderation_notes: Optional[str] = None
