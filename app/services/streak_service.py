from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.crud import habit as crud_habit
from app.crud import streak as crud_streak

class StreakService:
    @staticmethod
    def calculate_streak(db: Session, habit_id: int):
        if not crud_habit.get_habit_by_id(db, habit_id):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Habit not found")
            
        logs = crud_streak.get_all_logs_for_streak(db, habit_id)
        current_streak, max_streak, running_streak = 0, 0, 0
        
        for log in logs:
            if log.completed:
                running_streak += 1
                max_streak = max(max_streak, running_streak)
            else:
                running_streak = 0
                
        if logs and logs[-1].completed:
            current_streak = running_streak
            
        return {"habit_id": habit_id, "current_streak": current_streak, "max_streak": max_streak}