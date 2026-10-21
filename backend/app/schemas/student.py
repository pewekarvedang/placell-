from typing import Optional, List
from pydantic import BaseModel, Field, ConfigDict
from app.schemas.skill import StudentSkillItem

class StudentProfileUpdate(BaseModel):
    cgpa: Optional[float] = Field(None, ge=0.0, le=10.0)
    graduation_year: Optional[int] = None
    projects_count: Optional[int] = Field(None, ge=0)
    internships_count: Optional[int] = Field(None, ge=0)
    certifications_count: Optional[int] = Field(None, ge=0)
    preferred_role_title: Optional[str] = None
    bio: Optional[str] = None
    resume_url: Optional[str] = None

class StudentProfileResponse(BaseModel):
    id: str
    user_id: str
    roll_number: str
    full_name: str
    email: str
    department_id: str
    department_code: str
    department_name: str
    cgpa: float
    graduation_year: int
    projects_count: int
    internships_count: int
    certifications_count: int
    preferred_role_title: str
    bio: Optional[str] = None
    resume_url: Optional[str] = None
    skills: List[StudentSkillItem] = []

    model_config = ConfigDict(from_attributes=True)

class StudentGapAnalysisResponse(BaseModel):
    target_role: str
    matched_skills: List[str]
    missing_skills: List[str]
    match_percentage: float
    recommendations: List[dict]
