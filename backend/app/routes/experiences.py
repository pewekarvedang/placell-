from typing import List, Optional
from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.dependencies import get_current_user, RequireRoles
from app.models.user import User, UserRole
from app.models.experience import ExperienceStatus
from app.schemas.experience import ExperienceCreate, ExperienceResponse, ExperienceModeration
from app.services.experience_service import (
    submit_placement_experience,
    get_experiences,
    get_student_experiences,
    moderate_experience
)

router = APIRouter(prefix="/experiences", tags=["Placement Experiences"])

@router.get("", response_model=List[ExperienceResponse])
def list_verified_experiences(
    company_id: Optional[str] = None,
    search: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Retrieve verified placement experiences knowledge base."""
    return get_experiences(db, company_id=company_id, status_filter=ExperienceStatus.VERIFIED, search=search)

@router.get("/my", response_model=List[ExperienceResponse])
def get_my_experiences(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Retrieve all experiences submitted by the current student."""
    return get_student_experiences(db, current_user.id)

@router.get("/pending", response_model=List[ExperienceResponse])
def get_pending_moderation(
    current_user: User = Depends(RequireRoles([UserRole.ADMIN, UserRole.TPO])),
    db: Session = Depends(get_db)
):
    """(TPO / Admin) Moderation queue of pending student submissions."""
    return get_experiences(db, status_filter=ExperienceStatus.PENDING)

@router.post("", response_model=ExperienceResponse)
def create_experience(
    data: ExperienceCreate,
    request: Request,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """(Student) Submit an interview experience, automatically executing ASTMA NLP processing."""
    client_ip = request.client.host if request.client else None
    return submit_placement_experience(db, current_user.id, data, ip_address=client_ip)

@router.patch("/{experience_id}/verify", response_model=ExperienceResponse)
def verify_or_reject_experience(
    experience_id: str,
    data: ExperienceModeration,
    current_user: User = Depends(RequireRoles([UserRole.ADMIN, UserRole.TPO])),
    db: Session = Depends(get_db)
):
    """(TPO / Admin) Approve or reject a submitted placement experience."""
    return moderate_experience(db, current_user.id, experience_id, data)
