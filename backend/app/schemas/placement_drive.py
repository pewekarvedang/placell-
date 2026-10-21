from datetime import date
from typing import Optional, List
from pydantic import BaseModel, ConfigDict
from app.models.placement_drive import DriveStatus, ApplicationStatus

class DriveBase(BaseModel):
    company_id: str
    job_role_id: str
    title: str
    drive_date: date
    status: DriveStatus = DriveStatus.UPCOMING
    eligibility_cgpa: float = 6.5
    eligibility_criteria: Optional[str] = None
    ctc_offered_lpa: float = 6.0
    rounds_description: Optional[str] = None

class DriveCreate(DriveBase):
    pass

class DriveResponse(DriveBase):
    id: str
    company_name: str
    job_role_title: str
    applicants_count: int = 0
    selected_count: int = 0
    model_config = ConfigDict(from_attributes=True)

class ApplicationResponse(BaseModel):
    id: str
    placement_drive_id: str
    drive_title: str
    company_name: str
    student_id: str
    student_name: str
    student_roll_number: str
    student_cgpa: float
    status: ApplicationStatus
    model_config = ConfigDict(from_attributes=True)

class ApplicationStatusUpdate(BaseModel):
    status: ApplicationStatus
