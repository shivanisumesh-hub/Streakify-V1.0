from sqlalchemy.orm import Session

from app.models.habit import Habit
from app.schemas.habit import HabitCreate


def create_habit(db: Session, habit: HabitCreate):
    db_habit = Habit(
        name=habit.name,
        target_days_per_week=habit.target_days_per_week,
        user_id=habit.user_id
    )

    db.add(db_habit)
    db.commit()
    db.refresh(db_habit)

    return db_habit


def get_habit(db: Session, habit_id: int):
    return (
        db.query(Habit)
        .filter(Habit.id == habit_id)
        .first()
    )


def get_user_habits(db: Session, user_id: int):
    return (
        db.query(Habit)
        .filter(Habit.user_id == user_id)
        .all()
    )


def delete_habit(db: Session, habit_id: int):
    habit = get_habit(db, habit_id)

    if not habit:
        return None

    db.delete(habit)
    db.commit()

    return habit