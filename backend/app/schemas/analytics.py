from typing import List, Dict, Any, Optional
from pydantic import BaseModel

class DashboardKPIs(BaseModel):
    total_students: int
    total_companies: int
    total_drives: int
    total_experiences: int
    overall_placement_rate: float
    average_experience_rating: float
    average_interview_difficulty: float
    verified_experiences_count: int

class SentimentDistribution(BaseModel):
    positive: float
    neutral: float
    negative: float
    positive_count: int
    neutral_count: int
    negative_count: int

class SkillDemandItem(BaseModel):
    skill_name: str
    category: str
    mention_count: int
    percentage: float

class DepartmentMetric(BaseModel):
    department_code: str
    department_name: str
    total_students: int
    placed_students: int
    placement_rate: float
    average_cgpa: float
    average_readiness: float
    top_skill_gaps: List[str]

class OverviewAnalyticsResponse(BaseModel):
    kpis: DashboardKPIs
    sentiment_distribution: SentimentDistribution
    top_demanded_skills: List[SkillDemandItem]
    top_hiring_companies: List[Dict[str, Any]]
    interview_difficulty_breakdown: Dict[str, int]
    department_metrics: List[DepartmentMetric]
    monthly_placement_trends: List[Dict[str, Any]]
