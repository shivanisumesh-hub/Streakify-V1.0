from fastapi import HTTPException

from app.crud.habit import get_habit
from app.crud.habit_log import get_habit_logs
from app.crud.streak import calculate_streak


def get_streak_service(
    db,
    habit_id
):
    habit = get_habit(
        db,
        habit_id
    )

    if not habit:
        raise HTTPException(
            status_code=404,
            detail="Habit not found"
        )

    logs = get_habit_logs(
        db,
        habit_id
    )

    return calculate_streak(
        logs
    )