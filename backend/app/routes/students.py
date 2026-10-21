from typing import Optional
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.models.user import User
from app.schemas.student import StudentProfileResponse, StudentProfileUpdate, StudentGapAnalysisResponse
from app.schemas.skill import StudentSkillAdd
from app.services.student_service import (
    get_student_by_user_id,
    format_student_profile,
    update_student_profile,
    add_skill_to_student,
    remove_skill_from_student,
    calculate_student_gap_analysis,
    evaluate_and_record_readiness
)

router = APIRouter(prefix="/students", tags=["Students"])

@router.get("/me", response_model=StudentProfileResponse)
def get_my_profile(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Retrieve the logged-in student's full academic and skills profile."""
    student = get_student_by_user_id(db, current_user.id)
    return format_student_profile(student)

@router.put("/me", response_model=StudentProfileResponse)
def update_my_profile(
    data: StudentProfileUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update profile metrics (CGPA, projects, certifications, target roles)."""
    return update_student_profile(db, current_user.id, data)

@router.post("/me/skills", response_model=StudentProfileResponse)
def add_skill(
    data: StudentSkillAdd,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Associate a technical/soft skill with the student profile."""
    return add_skill_to_student(db, current_user.id, data.skill_id, data.proficiency_level)

@router.delete("/me/skills/{skill_id}", response_model=StudentProfileResponse)
def remove_skill(
    skill_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Remove a skill from the student profile."""
    return remove_skill_from_student(db, current_user.id, skill_id)

@router.get("/me/readiness")
def get_readiness_score(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Execute ASTMA Placement Readiness evaluation for the logged-in student."""
    student = get_student_by_user_id(db, current_user.id)
    return evaluate_and_record_readiness(db, student.id)

@router.get("/me/skill-gap", response_model=StudentGapAnalysisResponse)
def get_skill_gap(
    target_role_id: Optional[str] = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Execute Explainable Skill Gap Analyzer matching student skills against industry requirements."""
    student = get_student_by_user_id(db, current_user.id)
    return calculate_student_gap_analysis(db, student.id, target_role_id)
