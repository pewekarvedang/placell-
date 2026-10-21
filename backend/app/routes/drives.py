from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.dependencies import get_current_user, RequireRoles
from app.models.user import User, UserRole
from app.models.placement_drive import PlacementDrive, DriveStatus, Application, ApplicationStatus
from app.schemas.placement_drive import DriveCreate, DriveResponse, ApplicationResponse, ApplicationStatusUpdate
from app.services.drive_service import get_drives, create_drive, apply_student_to_drive

router = APIRouter(prefix="/drives", tags=["Placement Drives"])

@router.get("", response_model=List[DriveResponse])
def list_drives(
    status: Optional[DriveStatus] = None,
    company_id: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Retrieve catalog of scheduled, active, and completed placement drives."""
    return get_drives(db, status, company_id)

@router.post("", response_model=DriveResponse)
def add_drive(
    data: DriveCreate,
    current_user: User = Depends(RequireRoles([UserRole.ADMIN, UserRole.TPO])),
    db: Session = Depends(get_db)
):
    """(Admin / TPO) Schedule a new campus placement drive."""
    return create_drive(db, data)

@router.post("/{drive_id}/apply", response_model=ApplicationResponse)
def apply_to_drive(
    drive_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """(Student) Submit application for an active placement drive."""
    return apply_student_to_drive(db, current_user.id, drive_id)

@router.get("/{drive_id}/applications", response_model=List[ApplicationResponse])
def get_drive_applications(
    drive_id: str,
    current_user: User = Depends(RequireRoles([UserRole.ADMIN, UserRole.TPO, UserRole.FACULTY])),
    db: Session = Depends(get_db)
):
    """(TPO / Faculty / Admin) View all student applicants for a drive."""
    apps = db.query(Application).filter(Application.placement_drive_id == drive_id).all()
    results: List[ApplicationResponse] = []
    for a in apps:
        results.append(ApplicationResponse(
            id=a.id,
            placement_drive_id=a.placement_drive_id,
            drive_title=a.placement_drive.title,
            company_name=a.placement_drive.company.name if a.placement_drive.company else "",
            student_id=a.student_id,
            student_name=a.student.user.full_name if a.student and a.student.user else "Student",
            student_roll_number=a.student.roll_number if a.student else "N/A",
            student_cgpa=a.student.cgpa if a.student else 0.0,
            status=a.status
        ))
    return results

@router.patch("/applications/{application_id}/status", response_model=ApplicationResponse)
def update_application_status(
    application_id: str,
    data: ApplicationStatusUpdate,
    current_user: User = Depends(RequireRoles([UserRole.ADMIN, UserRole.TPO])),
    db: Session = Depends(get_db)
):
    """(Admin / TPO) Update applicant status (Shortlisted, Interviewed, Selected, Rejected)."""
    app = db.query(Application).filter(Application.id == application_id).first()
    if not app:
        raise HTTPException(status_code=404, detail="Application not found")
    app.status = data.status
    db.commit()
    db.refresh(app)
    return ApplicationResponse(
        id=app.id,
        placement_drive_id=app.placement_drive_id,
        drive_title=app.placement_drive.title,
        company_name=app.placement_drive.company.name if app.placement_drive.company else "",
        student_id=app.student_id,
        student_name=app.student.user.full_name if app.student and app.student.user else "Student",
        student_roll_number=app.student.roll_number if app.student else "N/A",
        student_cgpa=app.student.cgpa if app.student else 0.0,
        status=app.status
    )
