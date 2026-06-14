from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.config import get_db
from app.crud.habit import get_habit
from app.crud.habit_log import get_habit_logs
from app.crud.streak import calculate_streak

router = APIRouter(
    tags=["Streaks"]
)


@router.get("/habits/{habit_id}/streak")
def get_streak(
    habit_id: int,
    db: Session = Depends(get_db)
):
    habit = get_habit(db, habit_id)

    if not habit:
        raise HTTPException(
            status_code=404,
            detail="Habit not found"
        )

    logs = get_habit_logs(
        db,
        habit_id
    )

    return calculate_streak(logs)