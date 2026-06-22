from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from datetime import date, datetime
from app.crud import habit as crud_habit
from app.crud import habit_log as crud_log
from app.schemas.habit_log import HabitLogCreate, HabitLogUpdate

class HabitLogService:
    @staticmethod
    def create_log(db: Session, habit_id: int, payload: HabitLogCreate):
        if not crud_habit.get_habit_by_id(db, habit_id):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Habit not found")
        
        target_date = payload.log_date or date.today()
        if target_date > date.today():
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Cannot log habits for a future date")

        if crud_log.get_log_by_date(db, habit_id, target_date):
            detail = "Habit already logged for today" if target_date == date.today() else "Habit already logged for this date"
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)
            
        return crud_log.create_log(db, habit_id, target_date, payload.completed)

    @staticmethod
    def update_log(db: Session, habit_id: int, date_str: str, payload: HabitLogUpdate):
        try:
            target_date = datetime.strptime(date_str, "%Y-%m-%d").date()
        except ValueError:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid date format. Use YYYY-MM-DD")
            
        if target_date > date.today():
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Cannot log habits for a future date")
            
        db_log = crud_log.get_log_by_date(db, habit_id, target_date)
        if not db_log:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Log entry not found")
            
        db_log.completed = payload.completed
        db.commit()
        db.refresh(db_log)
        return db_log

    @staticmethod
    def get_logs(db: Session, habit_id: int):
        if not crud_habit.get_habit_by_id(db, habit_id):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Habit not found")
        return crud_log.get_habit_logs_sorted(db, habit_id)
