from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.config import get_db
from app.crud.habit import (
    create_habit,
    get_habit,
    get_user_habits,
    delete_habit
)
from app.crud.user import get_user
from app.schemas.habit import (
    HabitCreate,
    HabitResponse
)

router = APIRouter(
    prefix="",
    tags=["Habits"]
)


@router.post(
    "/habits",
    response_model=HabitResponse
)
def create_new_habit(
    habit: HabitCreate,
    db: Session = Depends(get_db)
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


@router.get(
    "/users/{user_id}/habits",
    response_model=list[HabitResponse]
)
def get_habits(
    user_id: int,
    db: Session = Depends(get_db)
):
    return get_user_habits(
        db,
        user_id
    )


@router.delete("/habits/{habit_id}")
def remove_habit(
    habit_id: int,
    db: Session = Depends(get_db)
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