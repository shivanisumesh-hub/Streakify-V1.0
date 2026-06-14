from datetime import date

from sqlalchemy.orm import Session

from app.models.habit_log import HabitLog
from app.schemas.habit_log import HabitLogCreate


def get_log_by_date(
    db: Session,
    habit_id: int,
    log_date: date
):
    return (
        db.query(HabitLog)
        .filter(
            HabitLog.habit_id == habit_id,
            HabitLog.log_date == log_date
        )
        .first()
    )


def create_log(
    db: Session,
    habit_id: int,
    log: HabitLogCreate
):
    db_log = HabitLog(
        habit_id=habit_id,
        log_date=log.log_date,
        completed=log.completed
    )

    db.add(db_log)
    db.commit()
    db.refresh(db_log)

    return db_log


def update_log(
    db: Session,
    habit_id: int,
    log_date: date,
    completed: bool
):
    log = (
        db.query(HabitLog)
        .filter(
            HabitLog.habit_id == habit_id,
            HabitLog.log_date == log_date
        )
        .first()
    )

    if not log:
        return None

    log.completed = completed

    db.commit()
    db.refresh(log)

    return log


def get_habit_logs(
    db: Session,
    habit_id: int
):
    return (
        db.query(HabitLog)
        .filter(HabitLog.habit_id == habit_id)
        .order_by(HabitLog.log_date)
        .all()
    )