from typing import Dict, Any, List
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.student import Student, StudentSkill
from app.models.skill import Skill
from app.models.company import JobRole, JobRoleSkill
from app.models.ai_results import ReadinessEvaluation, Recommendation
from app.schemas.student import StudentProfileUpdate, StudentProfileResponse
from app.schemas.skill import StudentSkillItem
from app.ai.readiness_model import readiness_model
from app.ai.recommendation_engine import recommendation_engine

def get_student_by_user_id(db: Session, user_id: str) -> Student:
    student = db.query(Student).filter(Student.user_id == user_id).first()
    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student profile not found for the authenticated user"
        )
    return student

def format_student_profile(student: Student) -> StudentProfileResponse:
    skills_list: List[StudentSkillItem] = []
    for ss in student.skills:
        skills_list.append(StudentSkillItem(
            skill_id=ss.skill.id,
            skill_name=ss.skill.name,
            category=ss.skill.category,
            proficiency_level=ss.proficiency_level
        ))

    return StudentProfileResponse(
        id=student.id,
        user_id=student.user_id,
        roll_number=student.roll_number,
        full_name=student.user.full_name,
        email=student.user.email,
        department_id=student.department_id,
        department_code=student.department.code if student.department else "N/A",
        department_name=student.department.name if student.department else "N/A",
        cgpa=student.cgpa,
        graduation_year=student.graduation_year,
        projects_count=student.projects_count,
        internships_count=student.internships_count,
        certifications_count=student.certifications_count,
        preferred_role_title=student.preferred_role_title,
        bio=student.bio,
        resume_url=student.resume_url,
        skills=skills_list
    )

def update_student_profile(db: Session, user_id: str, data: StudentProfileUpdate) -> StudentProfileResponse:
    student = get_student_by_user_id(db, user_id)
    update_dict = data.model_dump(exclude_unset=True)
    for field, val in update_dict.items():
        setattr(student, field, val)
    db.commit()
    db.refresh(student)
    return format_student_profile(student)

def add_skill_to_student(db: Session, user_id: str, skill_id: str, proficiency: str = "Intermediate") -> StudentProfileResponse:
    student = get_student_by_user_id(db, user_id)
    skill = db.query(Skill).filter(Skill.id == skill_id).first()
    if not skill:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Skill not found")

    existing = db.query(StudentSkill).filter(
        StudentSkill.student_id == student.id,
        StudentSkill.skill_id == skill_id
    ).first()

    if existing:
        existing.proficiency_level = proficiency
    else:
        new_ss = StudentSkill(student_id=student.id, skill_id=skill_id, proficiency_level=proficiency)
        db.add(new_ss)

    db.commit()
    db.refresh(student)
    return format_student_profile(student)

def remove_skill_from_student(db: Session, user_id: str, skill_id: str) -> StudentProfileResponse:
    student = get_student_by_user_id(db, user_id)
    existing = db.query(StudentSkill).filter(
        StudentSkill.student_id == student.id,
        StudentSkill.skill_id == skill_id
    ).first()
    if existing:
        db.delete(existing)
        db.commit()
        db.refresh(student)
    return format_student_profile(student)

def calculate_student_gap_analysis(db: Session, student_id: str, target_role_id: str = None) -> Dict[str, Any]:
    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    student_skills = [ss.skill.name for ss in student.skills]

    # Resolve target role
    target_role = None
    if target_role_id:
        target_role = db.query(JobRole).filter(JobRole.id == target_role_id).first()
    
    if not target_role:
        # Match by preferred role title or fallback to first job role
        target_role = db.query(JobRole).filter(JobRole.title.ilike(f"%{student.preferred_role_title}%")).first()
        if not target_role:
            target_role = db.query(JobRole).first()

    required_skills: List[str] = []
    role_title = student.preferred_role_title
    if target_role:
        role_title = f"{target_role.title} ({target_role.company.name})"
        required_skills = [jrs.skill.name for jrs in target_role.skills]

    if not required_skills:
        # Default benchmark for standard SDE
        required_skills = ["Data Structures", "Algorithms", "SQL", "DBMS", "REST APIs", "Python", "Git", "System Design"]

    gap_result = recommendation_engine.analyze_gap(
        student_skills=student_skills,
        required_skills=required_skills,
        target_role_title=role_title
    )
    return gap_result

def evaluate_and_record_readiness(db: Session, student_id: str) -> Dict[str, Any]:
    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    student_skills = [ss.skill.name for ss in student.skills]

    # Target role skills
    target_role = db.query(JobRole).filter(JobRole.title.ilike(f"%{student.preferred_role_title}%")).first()
    target_role_skills = [jrs.skill.name for jrs in target_role.skills] if target_role else []

    evaluation = readiness_model.evaluate(
        cgpa=student.cgpa,
        student_skills=student_skills,
        target_role_skills=target_role_skills,
        projects_count=student.projects_count,
        internships_count=student.internships_count,
        certifications_count=student.certifications_count
    )

    # Persist or update readiness evaluation record
    existing = db.query(ReadinessEvaluation).filter(ReadinessEvaluation.student_id == student.id).first()
    if existing:
        existing.readiness_percentage = evaluation["readiness_percentage"]
        existing.readiness_tier = evaluation["readiness_tier"]
        existing.feature_breakdown = evaluation["feature_breakdown"]
    else:
        new_eval = ReadinessEvaluation(
            student_id=student.id,
            readiness_percentage=evaluation["readiness_percentage"],
            readiness_tier=evaluation["readiness_tier"],
            feature_breakdown=evaluation["feature_breakdown"]
        )
        db.add(new_eval)

    db.commit()
    return evaluation
