from sqlalchemy.orm import Session
from app.models.habit_log import HabitLog

def get_all_logs_for_streak(db: Session, habit_id: int):
    return db.query(HabitLog).filter(HabitLog.habit_id == habit_id).order_by(HabitLog.log_date.asc()).all()