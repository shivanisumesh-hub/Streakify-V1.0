from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List
from app.schemas.habit_log import HabitLogCreate, HabitLogResponse, HabitLogUpdate
from app.services.habit_log_service import HabitLogService
from app.config import get_db

router = APIRouter(prefix="/habits/{habitId}/logs", tags=["Habit Logs"])

@router.post("", response_model=HabitLogResponse, status_code=status.HTTP_201_CREATED)
def log_habit(habitId: int, payload: HabitLogCreate, db: Session = Depends(get_db)):
    return HabitLogService.create_log(db, habitId, payload)

@router.put("/{date_str}", response_model=HabitLogResponse)
def update_habit_log(habitId: int, date_str: str, payload: HabitLogUpdate, db: Session = Depends(get_db)):
    return HabitLogService.update_log(db, habitId, date_str, payload)

@router.get("", response_model=List[HabitLogResponse])
def get_logs(habitId: int, db: Session = Depends(get_db)):
    return HabitLogService.get_logs(db, habitId)