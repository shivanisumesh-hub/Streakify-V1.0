from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List
from app.schemas.habit import HabitCreate, HabitResponse
from app.services.habit_service import HabitService
from app.config import get_db

router = APIRouter(tags=["Habits"])

@router.post("/habits", response_model=HabitResponse, status_code=status.HTTP_201_CREATED)
def create_habit(habit: HabitCreate, db: Session = Depends(get_db)):
    return HabitService.create_habit(db, habit)

@router.get("/users/{userId}/habits", response_model=List[HabitResponse])
def get_user_habits(userId: int, db: Session = Depends(get_db)):
    return HabitService.get_user_habits(db, userId)

@router.delete("/habits/{id}")
def delete_habit(id: int, db: Session = Depends(get_db)):
    return HabitService.delete_habit(db, id)