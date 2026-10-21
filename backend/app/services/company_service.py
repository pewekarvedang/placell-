from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.company import Company, JobRole, JobRoleSkill
from app.models.experience import PlacementExperience, ExperienceStatus
from app.models.ai_results import NLPAnalysisResult
from app.schemas.company import CompanyCreate, CompanyAnalyticsResponse, JobRoleCreate

def get_companies(db: Session, search: Optional[str] = None, industry: Optional[str] = None) -> List[Company]:
    query = db.query(Company)
    if search:
        query = query.filter(Company.name.ilike(f"%{search}%"))
    if industry:
        query = query.filter(Company.industry == industry)
    return query.order_by(Company.name).all()

def create_company(db: Session, data: CompanyCreate) -> Company:
    existing = db.query(Company).filter(Company.name == data.name).first()
    if existing:
        raise HTTPException(status_code=400, detail="Company with this name already exists")
    
    company = Company(**data.model_dump())
    db.add(company)
    db.commit()
    db.refresh(company)
    return company

def create_job_role(db: Session, data: JobRoleCreate) -> JobRole:
    company = db.query(Company).filter(Company.id == data.company_id).first()
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")

    role = JobRole(
        company_id=data.company_id,
        title=data.title,
        min_cgpa=data.min_cgpa,
        description=data.description
    )
    db.add(role)
    db.flush()

    for skill_id in data.required_skill_ids:
        jrs = JobRoleSkill(job_role_id=role.id, skill_id=skill_id)
        db.add(jrs)

    db.commit()
    db.refresh(role)
    return role

def get_company_analytics(db: Session, company_id: str) -> CompanyAnalyticsResponse:
    company = db.query(Company).filter(Company.id == company_id).first()
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")

    experiences = db.query(PlacementExperience).filter(
        PlacementExperience.company_id == company.id,
        PlacementExperience.status == ExperienceStatus.VERIFIED
    ).all()

    total_exp = len(experiences)
    if total_exp == 0:
        return CompanyAnalyticsResponse(
            company_id=company.id,
            company_name=company.name,
            industry=company.industry,
            total_experiences=0,
            average_overall_rating=4.0,
            average_difficulty_rating=3.0,
            average_rounds_count=3,
            positive_sentiment_percent=80.0,
            neutral_sentiment_percent=15.0,
            negative_sentiment_percent=5.0,
            top_demanded_skills=[{"skill": "Data Structures", "count": 1}, {"skill": "SQL", "count": 1}],
            frequent_interview_topics=["Technical Coding", "System Design"],
            common_rounds=[{"type": "CODING", "count": 1}, {"type": "TECHNICAL_INTERVIEW", "count": 1}]
        )

    avg_rating = sum(e.overall_rating for e in experiences) / total_exp
    avg_diff = sum(e.difficulty_rating for e in experiences) / total_exp
    avg_rounds = int(sum(e.rounds_count for e in experiences) / total_exp)

    # Sentiment distribution
    pos_count = 0
    neu_count = 0
    neg_count = 0
    skill_freq: Dict[str, int] = {}
    topic_freq: Dict[str, int] = {}
    round_freq: Dict[str, int] = {}

    for e in experiences:
        if e.nlp_result:
            if e.nlp_result.sentiment_label == "POSITIVE":
                pos_count += 1
            elif e.nlp_result.sentiment_label == "NEGATIVE":
                neg_count += 1
            else:
                neu_count += 1

            for s in (e.nlp_result.extracted_skills or []):
                skill_freq[s] = skill_freq.get(s, 0) + 1

            for t in (e.nlp_result.extracted_topics or []):
                topic_freq[t] = topic_freq.get(t, 0) + 1
        else:
            neu_count += 1

        for r in e.rounds:
            rtype = r.round_type.value if hasattr(r.round_type, 'value') else str(r.round_type)
            round_freq[rtype] = round_freq.get(rtype, 0) + 1

    pos_pct = round((pos_count / total_exp) * 100.0, 1)
    neu_pct = round((neu_count / total_exp) * 100.0, 1)
    neg_pct = round((neg_count / total_exp) * 100.0, 1)

    top_skills = [{"skill": k, "count": v} for k, v in sorted(skill_freq.items(), key=lambda x: x[1], reverse=True)[:8]]
    top_topics = [k for k, _ in sorted(topic_freq.items(), key=lambda x: x[1], reverse=True)[:6]]
    common_rounds = [{"type": k, "count": v} for k, v in sorted(round_freq.items(), key=lambda x: x[1], reverse=True)]

    return CompanyAnalyticsResponse(
        company_id=company.id,
        company_name=company.name,
        industry=company.industry,
        total_experiences=total_exp,
        average_overall_rating=round(avg_rating, 1),
        average_difficulty_rating=round(avg_diff, 1),
        average_rounds_count=max(1, avg_rounds),
        positive_sentiment_percent=pos_pct,
        neutral_sentiment_percent=neu_pct,
        negative_sentiment_percent=neg_pct,
        top_demanded_skills=top_skills,
        frequent_interview_topics=top_topics,
        common_rounds=common_rounds
    )
