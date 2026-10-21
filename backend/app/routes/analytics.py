from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.analytics import OverviewAnalyticsResponse
from app.services.analytics_service import get_overview_analytics

router = APIRouter(prefix="/analytics", tags=["Analytics"])

@router.get("/overview", response_model=OverviewAnalyticsResponse)
def get_analytics_overview(db: Session = Depends(get_db)):
    """Retrieve college-wide placement analytics, sentiment distributions, and department metrics."""
    return get_overview_analytics(db)
