from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.models.user import User
from app.schemas.auth import LoginRequest, RegisterRequest, Token, UserResponse, ChangePasswordRequest
from app.services.auth_service import authenticate_user, register_student
from app.core.security import verify_password, get_password_hash
from app.services.audit_service import log_action

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/login", response_model=Token)
def login(credentials: LoginRequest, db: Session = Depends(get_db)):
    """Authenticate user with email and password, issuing a signed JWT."""
    token = authenticate_user(db, credentials)
    log_action(
        db=db,
        action="USER_LOGIN",
        entity_name="User",
        user_id=token.user_id,
        details=f"User {credentials.email} logged in successfully."
    )
    return token

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register(data: RegisterRequest, db: Session = Depends(get_db)):
    """Self-registration endpoint for students."""
    user = register_student(db, data)
    log_action(
        db=db,
        action="STUDENT_REGISTRATION",
        entity_name="User",
        user_id=user.id,
        details=f"Student registered with roll number {data.roll_number}."
    )
    return UserResponse(
        id=user.id,
        email=user.email,
        full_name=user.full_name,
        role=user.role,
        is_active=user.is_active,
        department_id=user.department_id,
        department_name=user.department.name if user.department else None
    )

@router.get("/me", response_model=UserResponse)
def get_current_user_profile(current_user: User = Depends(get_current_user)):
    """Retrieve identity and permissions of the currently authenticated user."""
    return UserResponse(
        id=current_user.id,
        email=current_user.email,
        full_name=current_user.full_name,
        role=current_user.role,
        is_active=current_user.is_active,
        department_id=current_user.department_id,
        department_name=current_user.department.name if current_user.department else None
    )

@router.post("/change-password")
def change_password(data: ChangePasswordRequest, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Rotate credentials securely for authenticated session."""
    if not verify_password(data.current_password, current_user.hashed_password):
        raise HTTPException(status_code=400, detail="Current password is incorrect")
    current_user.hashed_password = get_password_hash(data.new_password)
    db.commit()
    log_action(
        db=db,
        action="CHANGE_PASSWORD",
        entity_name="User",
        user_id=current_user.id,
        details="Password changed successfully"
    )
    return {"message": "Password updated successfully"}
