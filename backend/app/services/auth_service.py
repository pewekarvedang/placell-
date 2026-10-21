from typing import Optional
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.user import User, UserRole
from app.models.student import Student
from app.core.security import verify_password, get_password_hash, create_access_token
from app.schemas.auth import LoginRequest, RegisterRequest, Token

def authenticate_user(db: Session, credentials: LoginRequest) -> Token:
    """Authenticates user and returns JWT token payload."""
    user = db.query(User).filter(User.email == credentials.email).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if not verify_password(credentials.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is deactivated. Contact administrator.",
        )

    dept_code = user.department.code if user.department else None

    token_str = create_access_token(subject=user.id, role=user.role.value)
    return Token(
        access_token=token_str,
        token_type="bearer",
        role=user.role,
        user_id=user.id,
        email=user.email,
        full_name=user.full_name,
        department_id=user.department_id,
        department_code=dept_code
    )

def register_student(db: Session, data: RegisterRequest) -> User:
    """Registers a new student user and creates the associated student profile."""
    existing_user = db.query(User).filter(User.email == data.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A user with this email address already exists"
        )
    
    existing_roll = db.query(Student).filter(Student.roll_number == data.roll_number).first()
    if existing_roll:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A student with this roll number is already registered"
        )

    user = User(
        email=data.email,
        hashed_password=get_password_hash(data.password),
        full_name=data.full_name,
        role=UserRole.STUDENT,
        department_id=data.department_id,
        is_active=True
    )
    db.add(user)
    db.flush()

    student = Student(
        user_id=user.id,
        roll_number=data.roll_number,
        department_id=data.department_id,
        graduation_year=data.graduation_year,
        cgpa=data.cgpa,
        preferred_role_title="Software Development Engineer"
    )
    db.add(student)
    db.commit()
    db.refresh(user)
    return user
