from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas.habit_log import DashboardResponse
from app.services.dashboard_service import DashboardService
from app.config import get_db

router = APIRouter(tags=["Dashboard"])

@router.get("/users/{userId}/dashboard", response_model=DashboardResponse)
def get_dashboard(userId: int, db: Session = Depends(get_db)):
    return DashboardService.generate_dashboard(db, userId)