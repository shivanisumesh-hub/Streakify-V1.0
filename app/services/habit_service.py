from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.crud import habit as crud_habit
from app.services.user_service import UserService
from app.schemas.habit import HabitCreate

class HabitService:
    @staticmethod
    def create_habit(db: Session, habit_data: HabitCreate):
        UserService.get_user(db, habit_data.user_id) # Enforce parent existence check
        return crud_habit.create_habit(db, habit_data)

    @staticmethod
    def get_user_habits(db: Session, user_id: int):
        UserService.get_user(db, user_id)
        return crud_habit.get_user_habits(db, user_id)

    @staticmethod
    def delete_habit(db: Session, habit_id: int):
        habit = crud_habit.get_habit_by_id(db, habit_id)
        if not habit:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Habit not found")
        crud_habit.delete_habit(db, habit)
        return {"message": f"Habit {habit_id} successfully deleted"}