from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.dependencies import RequireRoles
from app.models.user import User, UserRole
from app.models.department import Department
from app.models.skill import Skill
from app.models.audit_log import AuditLog
from app.schemas.auth import UserResponse
from app.schemas.skill import SkillCreate, SkillResponse
from app.schemas.audit import AuditLogResponse
from pydantic import BaseModel, ConfigDict

router = APIRouter(prefix="/admin", tags=["Administration"])

class DepartmentCreate(BaseModel):
    code: str
    name: str
    description: Optional[str] = None

class DepartmentResponse(BaseModel):
    id: str
    code: str
    name: str
    description: Optional[str] = None
    model_config = ConfigDict(from_attributes=True)

@router.get("/users", response_model=List[UserResponse])
def get_all_users(
    current_user: User = Depends(RequireRoles([UserRole.ADMIN])),
    db: Session = Depends(get_db)
):
    """(Admin) List all accounts across all 4 roles."""
    users = db.query(User).all()
    results: List[UserResponse] = []
    for u in users:
        results.append(UserResponse(
            id=u.id,
            email=u.email,
            full_name=u.full_name,
            role=u.role,
            is_active=u.is_active,
            department_id=u.department_id,
            department_name=u.department.name if u.department else None
        ))
    return results

@router.get("/departments", response_model=List[DepartmentResponse])
def get_departments(db: Session = Depends(get_db)):
    """List all academic departments."""
    return db.query(Department).all()

@router.post("/departments", response_model=DepartmentResponse)
def add_department(
    data: DepartmentCreate,
    current_user: User = Depends(RequireRoles([UserRole.ADMIN])),
    db: Session = Depends(get_db)
):
    """(Admin) Register a new academic department."""
    existing = db.query(Department).filter(Department.code == data.code).first()
    if existing:
        raise HTTPException(status_code=400, detail="Department code already exists")
    dept = Department(**data.model_dump())
    db.add(dept)
    db.commit()
    db.refresh(dept)
    return dept

@router.get("/skills", response_model=List[SkillResponse])
def get_skills_catalog(db: Session = Depends(get_db)):
    """List the central skills taxonomy."""
    return db.query(Skill).order_by(Skill.name).all()

@router.post("/skills", response_model=SkillResponse)
def add_skill_to_catalog(
    data: SkillCreate,
    current_user: User = Depends(RequireRoles([UserRole.ADMIN, UserRole.TPO])),
    db: Session = Depends(get_db)
):
    """(Admin / TPO) Add a new skill to the central dictionary."""
    existing = db.query(Skill).filter(Skill.name.ilike(data.name)).first()
    if existing:
        raise HTTPException(status_code=400, detail="Skill already exists in catalog")
    s = Skill(**data.model_dump())
    db.add(s)
    db.commit()
    db.refresh(s)
    return s

@router.get("/audit-logs", response_model=List[AuditLogResponse])
def get_audit_trail(
    limit: int = 100,
    current_user: User = Depends(RequireRoles([UserRole.ADMIN])),
    db: Session = Depends(get_db)
):
    """(Admin) View system-wide enterprise audit logs."""
    logs = db.query(AuditLog).order_by(AuditLog.timestamp.desc()).limit(limit).all()
    results: List[AuditLogResponse] = []
    for l in logs:
        results.append(AuditLogResponse(
            id=l.id,
            user_id=l.user_id,
            user_email=l.user.email if l.user else "System",
            user_role=l.user.role.value if l.user else "SYSTEM",
            action=l.action,
            entity_name=l.entity_name,
            entity_id=l.entity_id,
            details=l.details,
            ip_address=l.ip_address,
            timestamp=l.timestamp
        ))
    return results
