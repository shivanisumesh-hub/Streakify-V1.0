from sqlalchemy.orm import Session
from datetime import date
from app.models.habit_log import HabitLog

def get_log_by_date(db: Session, habit_id: int, log_date: date):
    return db.query(HabitLog).filter(HabitLog.habit_id == habit_id, HabitLog.log_date == log_date).first()

def get_habit_logs_sorted(db: Session, habit_id: int):
    return db.query(HabitLog).filter(HabitLog.habit_id == habit_id).order_by(HabitLog.log_date.asc()).all()

def create_log(db: Session, habit_id: int, log_date: date, completed: bool):
    db_log = HabitLog(habit_id=habit_id, log_date=log_date, completed=completed)
    db.add(db_log)
    db.commit()
    db.refresh(db_log)
    return db_log