from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from datetime import timedelta
from app.crud import habit as crud_habit
from app.crud import streak as crud_streak

class StreakService:
    @staticmethod
    def calculate_streak(db: Session, habit_id: int):
        if not crud_habit.get_habit_by_id(db, habit_id):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Habit not found")
            
        logs = crud_streak.get_all_logs_for_streak(db, habit_id)
        current_streak, max_streak = StreakService.calculate_from_logs(logs)
            
        return {"habit_id": habit_id, "current_streak": current_streak, "max_streak": max_streak}

    @staticmethod
    def calculate_from_logs(logs):
        current_streak, max_streak, running_streak = 0, 0, 0
        previous_date = None
        
        for log in logs:
            if previous_date and log.log_date != previous_date + timedelta(days=1):
                running_streak = 0

            if log.completed:
                running_streak += 1
                max_streak = max(max_streak, running_streak)
                current_streak = running_streak
            else:
                running_streak = 0
                current_streak = 0

            previous_date = log.log_date
                
        return current_streak, max_streak
