from fastapi import HTTPException

from app.crud.user import get_user
from app.crud.habit import (
    create_habit,
    get_user_habits,
    delete_habit
)


def create_habit_service(
    db,
    habit
):
    user = get_user(
        db,
        habit.user_id
    )

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return create_habit(
        db,
        habit
    )


def get_user_habits_service(
    db,
    user_id
):
    return get_user_habits(
        db,
        user_id
    )


def delete_habit_service(
    db,
    habit_id
):
    habit = delete_habit(
        db,
        habit_id
    )

    if not habit:
        raise HTTPException(
            status_code=404,
            detail="Habit not found"
        )

    return {
        "message": "Habit deleted successfully"
    }