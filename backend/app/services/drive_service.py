from typing import List, Optional
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.placement_drive import PlacementDrive, Application, DriveStatus, ApplicationStatus
from app.models.student import Student
from app.schemas.placement_drive import DriveCreate, ApplicationResponse, DriveResponse

def get_drives(db: Session, drive_status: Optional[DriveStatus] = None, company_id: Optional[str] = None) -> List[DriveResponse]:
    query = db.query(PlacementDrive)
    if drive_status:
        query = query.filter(PlacementDrive.status == drive_status)
    if company_id:
        query = query.filter(PlacementDrive.company_id == company_id)

    drives = query.order_by(PlacementDrive.drive_date.desc()).all()
    results: List[DriveResponse] = []
    for d in drives:
        selected = sum(1 for a in d.applications if a.status == ApplicationStatus.SELECTED)
        results.append(DriveResponse(
            id=d.id,
            company_id=d.company_id,
            company_name=d.company.name if d.company else "Unknown",
            job_role_id=d.job_role_id,
            job_role_title=d.job_role.title if d.job_role else "Unknown",
            title=d.title,
            drive_date=d.drive_date,
            status=d.status,
            eligibility_cgpa=d.eligibility_cgpa,
            eligibility_criteria=d.eligibility_criteria,
            ctc_offered_lpa=d.ctc_offered_lpa,
            rounds_description=d.rounds_description,
            applicants_count=len(d.applications),
            selected_count=selected
        ))
    return results

def create_drive(db: Session, data: DriveCreate) -> DriveResponse:
    drive = PlacementDrive(**data.model_dump())
    db.add(drive)
    db.commit()
    db.refresh(drive)
    return DriveResponse(
        id=drive.id,
        company_id=drive.company_id,
        company_name=drive.company.name if drive.company else "",
        job_role_id=drive.job_role_id,
        job_role_title=drive.job_role.title if drive.job_role else "",
        title=drive.title,
        drive_date=drive.drive_date,
        status=drive.status,
        eligibility_cgpa=drive.eligibility_cgpa,
        eligibility_criteria=drive.eligibility_criteria,
        ctc_offered_lpa=drive.ctc_offered_lpa,
        rounds_description=drive.rounds_description,
        applicants_count=0,
        selected_count=0
    )

def apply_student_to_drive(db: Session, user_id: str, drive_id: str) -> ApplicationResponse:
    student = db.query(Student).filter(Student.user_id == user_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student profile not found")

    drive = db.query(PlacementDrive).filter(PlacementDrive.id == drive_id).first()
    if not drive:
        raise HTTPException(status_code=404, detail="Placement drive not found")

    if drive.status not in [DriveStatus.UPCOMING, DriveStatus.ACTIVE]:
        raise HTTPException(status_code=400, detail="Drive is not open for applications")

    if student.cgpa < drive.eligibility_cgpa:
        raise HTTPException(
            status_code=400,
            detail=f"Ineligible: CGPA {student.cgpa} is below drive requirement {drive.eligibility_cgpa}"
        )

    existing = db.query(Application).filter(
        Application.placement_drive_id == drive.id,
        Application.student_id == student.id
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="Already applied to this placement drive")

    app = Application(
        placement_drive_id=drive.id,
        student_id=student.id,
        status=ApplicationStatus.APPLIED
    )
    db.add(app)
    db.commit()
    db.refresh(app)

    return ApplicationResponse(
        id=app.id,
        placement_drive_id=drive.id,
        drive_title=drive.title,
        company_name=drive.company.name if drive.company else "",
        student_id=student.id,
        student_name=student.user.full_name,
        student_roll_number=student.roll_number,
        student_cgpa=student.cgpa,
        status=app.status
    )
