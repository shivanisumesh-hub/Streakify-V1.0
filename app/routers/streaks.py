from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas.habit_log import StreakResponse
from app.services.streak_service import StreakService
from app.config import get_db

router = APIRouter(prefix="/habits/{habitId}/streak", tags=["Streak Engine"])

@router.get("", response_model=StreakResponse)
def get_habit_streak(habitId: int, db: Session = Depends(get_db)):
    return StreakService.calculate_streak(db, habitId)