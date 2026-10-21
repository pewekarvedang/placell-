from typing import Optional, List
from pydantic import BaseModel, Field, ConfigDict

class JobRoleBase(BaseModel):
    title: str
    min_cgpa: float = Field(6.0, ge=0.0, le=10.0)
    description: Optional[str] = None

class JobRoleCreate(JobRoleBase):
    company_id: str
    required_skill_ids: List[str] = []

class JobRoleResponse(JobRoleBase):
    id: str
    company_id: str
    required_skills: List[str] = []
    model_config = ConfigDict(from_attributes=True)

class CompanyBase(BaseModel):
    name: str
    industry: str
    company_type: str = "Product"
    website: Optional[str] = None
    location: Optional[str] = None
    ctc_min_lpa: float = 4.0
    ctc_max_lpa: float = 12.0
    description: Optional[str] = None

class CompanyCreate(CompanyBase):
    pass

class CompanyResponse(CompanyBase):
    id: str
    roles_count: int = 0
    experiences_count: int = 0
    average_difficulty: float = 0.0
    positive_sentiment_percent: float = 0.0
    model_config = ConfigDict(from_attributes=True)

class CompanyAnalyticsResponse(BaseModel):
    company_id: str
    company_name: str
    industry: str
    total_experiences: int
    average_overall_rating: float
    average_difficulty_rating: float
    average_rounds_count: int
    positive_sentiment_percent: float
    neutral_sentiment_percent: float
    negative_sentiment_percent: float
    top_demanded_skills: List[dict]
    frequent_interview_topics: List[str]
    common_rounds: List[dict]
