from typing import List, Optional
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.experience import PlacementExperience, InterviewRound, ExperienceStatus
from app.models.student import Student
from app.models.company import Company, JobRole
from app.models.ai_results import NLPAnalysisResult
from app.schemas.experience import ExperienceCreate, ExperienceResponse, RoundResponse, NLPResultResponse, ExperienceModeration
from app.ai.sentiment_analyzer import sentiment_analyzer
from app.ai.skill_extractor import skill_extractor
from app.ai.topic_analyzer import topic_analyzer
from app.services.audit_service import log_action

def submit_placement_experience(db: Session, user_id: str, data: ExperienceCreate, ip_address: Optional[str] = None) -> ExperienceResponse:
    student = db.query(Student).filter(Student.user_id == user_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student profile required to log placement experiences")

    company = db.query(Company).filter(Company.id == data.company_id).first()
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")

    experience = PlacementExperience(
        student_id=student.id,
        placement_drive_id=data.placement_drive_id,
        company_id=data.company_id,
        job_role_id=data.job_role_id,
        overall_rating=data.overall_rating,
        difficulty_rating=data.difficulty_rating,
        rounds_count=data.rounds_count,
        questions_asked=data.questions_asked,
        skills_tested=data.skills_tested,
        free_text_feedback=data.free_text_feedback,
        is_placed=data.is_placed,
        status=ExperienceStatus.VERIFIED  # Auto-verified or set to PENDING for moderation
    )
    db.add(experience)
    db.flush()

    # Add interview rounds if supplied
    for r in data.rounds:
        round_obj = InterviewRound(
            experience_id=experience.id,
            round_number=r.round_number,
            round_type=r.round_type,
            round_title=r.round_title,
            description=r.description,
            duration_minutes=r.duration_minutes,
            difficulty=r.difficulty
        )
        db.add(round_obj)

    # Trigger ASTMA NLP Pipeline
    # 1. Sentiment analysis
    sentiment_out = sentiment_analyzer.analyze(
        text=data.free_text_feedback,
        user_rating=data.overall_rating
    )

    # 2. Skill extraction
    extracted_skills = skill_extractor.extract_from_text(
        text=f"{data.free_text_feedback} {data.questions_asked or ''}",
        user_tagged_skills=data.skills_tested or ""
    )

    # 3. Topic & Difficulty inference
    topic_out = topic_analyzer.analyze_topics_and_difficulty(
        text=f"{data.free_text_feedback} {data.questions_asked or ''}",
        user_difficulty=data.difficulty_rating
    )

    nlp_result = NLPAnalysisResult(
        experience_id=experience.id,
        sentiment_label=sentiment_out["sentiment_label"],
        sentiment_score=sentiment_out["sentiment_score"],
        sentiment_confidence=sentiment_out["sentiment_confidence"],
        inferred_difficulty=topic_out["inferred_difficulty"],
        extracted_skills=extracted_skills,
        extracted_topics=topic_out["extracted_topics"],
        frequently_mentioned_terms=topic_out["frequently_mentioned_terms"]
    )
    db.add(nlp_result)

    # Audit logging
    log_action(
        db=db,
        action="SUBMIT_EXPERIENCE",
        entity_name="PlacementExperience",
        user_id=user_id,
        entity_id=experience.id,
        details=f"Submitted experience for {company.name} with {len(extracted_skills)} extracted skills",
        ip_address=ip_address
    )

    db.commit()
    db.refresh(experience)
    return format_experience_response(experience)

def get_experiences(
    db: Session,
    company_id: Optional[str] = None,
    status_filter: Optional[ExperienceStatus] = ExperienceStatus.VERIFIED,
    search: Optional[str] = None
) -> List[ExperienceResponse]:
    query = db.query(PlacementExperience)
    if status_filter:
        query = query.filter(PlacementExperience.status == status_filter)
    if company_id:
        query = query.filter(PlacementExperience.company_id == company_id)

    experiences = query.order_by(PlacementExperience.created_at.desc()).all()
    results = [format_experience_response(e) for e in experiences]
    if search:
        s_lower = search.lower()
        results = [
            r for r in results 
            if s_lower in r.company_name.lower() or 
               (r.job_role_title and s_lower in r.job_role_title.lower()) or
               s_lower in r.free_text_feedback.lower()
        ]
    return results

def get_student_experiences(db: Session, user_id: str) -> List[ExperienceResponse]:
    student = db.query(Student).filter(Student.user_id == user_id).first()
    if not student:
        return []
    experiences = db.query(PlacementExperience).filter(
        PlacementExperience.student_id == student.id
    ).order_by(PlacementExperience.created_at.desc()).all()
    return [format_experience_response(e) for e in experiences]

def moderate_experience(
    db: Session,
    moderator_user_id: str,
    experience_id: str,
    data: ExperienceModeration
) -> ExperienceResponse:
    experience = db.query(PlacementExperience).filter(PlacementExperience.id == experience_id).first()
    if not experience:
        raise HTTPException(status_code=404, detail="Experience record not found")

    experience.status = data.status
    experience.verified_by_user_id = moderator_user_id
    experience.moderation_notes = data.moderation_notes

    log_action(
        db=db,
        action=f"MODERATE_EXPERIENCE_{data.status.value}",
        entity_name="PlacementExperience",
        user_id=moderator_user_id,
        entity_id=experience.id,
        details=f"Status changed to {data.status.value}"
    )

    db.commit()
    db.refresh(experience)
    return format_experience_response(experience)

def format_experience_response(e: PlacementExperience) -> ExperienceResponse:
    rounds_dto = [
        RoundResponse(
            id=r.id,
            round_number=r.round_number,
            round_type=r.round_type,
            round_title=r.round_title,
            description=r.description,
            duration_minutes=r.duration_minutes,
            difficulty=r.difficulty
        )
        for r in e.rounds
    ]

    nlp_dto = None
    if e.nlp_result:
        nlp_dto = NLPResultResponse(
            sentiment_label=e.nlp_result.sentiment_label,
            sentiment_score=e.nlp_result.sentiment_score,
            sentiment_confidence=e.nlp_result.sentiment_confidence,
            inferred_difficulty=e.nlp_result.inferred_difficulty,
            extracted_skills=e.nlp_result.extracted_skills or [],
            extracted_topics=e.nlp_result.extracted_topics or [],
            frequently_mentioned_terms=e.nlp_result.frequently_mentioned_terms or []
        )

    return ExperienceResponse(
        id=e.id,
        student_id=e.student_id,
        student_roll_number=e.student.roll_number if e.student else "Anonymous",
        student_department=e.student.department.code if (e.student and e.student.department) else "N/A",
        company_id=e.company_id,
        company_name=e.company.name if e.company else "Unknown",
        job_role_id=e.job_role_id,
        job_role_title=e.job_role.title if e.job_role else "Software Engineer",
        overall_rating=e.overall_rating,
        difficulty_rating=e.difficulty_rating,
        rounds_count=e.rounds_count,
        questions_asked=e.questions_asked,
        skills_tested=e.skills_tested,
        free_text_feedback=e.free_text_feedback,
        is_placed=e.is_placed,
        status=e.status,
        created_at=e.created_at,
        rounds=rounds_dto,
        nlp_result=nlp_dto
    )
