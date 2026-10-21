from typing import List, Optional
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.dependencies import get_current_user, RequireRoles
from app.models.user import User, UserRole
from app.schemas.company import CompanyCreate, CompanyResponse, CompanyAnalyticsResponse, JobRoleCreate, JobRoleResponse
from app.services.company_service import get_companies, create_company, get_company_analytics, create_job_role
from app.models.company import JobRole

router = APIRouter(prefix="/companies", tags=["Companies"])

@router.get("", response_model=List[CompanyResponse])
def list_companies(
    search: Optional[str] = None,
    industry: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Retrieve catalog of corporate recruiters with basic stats."""
    companies = get_companies(db, search, industry)
    results: List[CompanyResponse] = []
    for c in companies:
        results.append(CompanyResponse(
            id=c.id,
            name=c.name,
            industry=c.industry,
            company_type=c.company_type,
            website=c.website,
            location=c.location,
            ctc_min_lpa=c.ctc_min_lpa,
            ctc_max_lpa=c.ctc_max_lpa,
            description=c.description,
            roles_count=len(c.job_roles),
            experiences_count=len(c.experiences),
            average_difficulty=3.5,
            positive_sentiment_percent=82.0
        ))
    return results

@router.post("", response_model=CompanyResponse)
def add_company(
    data: CompanyCreate,
    current_user: User = Depends(RequireRoles([UserRole.ADMIN, UserRole.TPO])),
    db: Session = Depends(get_db)
):
    """(Admin / TPO) Register a new recruiting organization."""
    c = create_company(db, data)
    return CompanyResponse(
        id=c.id,
        name=c.name,
        industry=c.industry,
        company_type=c.company_type,
        website=c.website,
        location=c.location,
        ctc_min_lpa=c.ctc_min_lpa,
        ctc_max_lpa=c.ctc_max_lpa,
        description=c.description,
        roles_count=0,
        experiences_count=0,
        average_difficulty=0.0,
        positive_sentiment_percent=0.0
    )

@router.get("/{company_id}/analytics", response_model=CompanyAnalyticsResponse)
def get_single_company_analytics(company_id: str, db: Session = Depends(get_db)):
    """Retrieve aggregated NLP sentiment, difficulty, and skill demands for a company."""
    return get_company_analytics(db, company_id)

@router.get("/{company_id}/roles", response_model=List[JobRoleResponse])
def get_company_roles(company_id: str, db: Session = Depends(get_db)):
    """Get all open job roles for a company."""
    roles = db.query(JobRole).filter(JobRole.company_id == company_id).all()
    out: List[JobRoleResponse] = []
    for r in roles:
        skills = [s.skill.name for s in r.skills]
        out.append(JobRoleResponse(
            id=r.id,
            company_id=r.company_id,
            title=r.title,
            min_cgpa=r.min_cgpa,
            description=r.description,
            required_skills=skills
        ))
    return out

@router.post("/roles", response_model=JobRoleResponse)
def add_job_role(
    data: JobRoleCreate,
    current_user: User = Depends(RequireRoles([UserRole.ADMIN, UserRole.TPO])),
    db: Session = Depends(get_db)
):
    """(Admin / TPO) Create a new job role benchmark for a company."""
    role = create_job_role(db, data)
    skills = [s.skill.name for s in role.skills]
    return JobRoleResponse(
        id=role.id,
        company_id=role.company_id,
        title=role.title,
        min_cgpa=role.min_cgpa,
        description=role.description,
        required_skills=skills
    )
