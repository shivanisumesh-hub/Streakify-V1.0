from datetime import date

from fastapi import (
    APIRouter,
    Depends,
    HTTPException
)
from sqlalchemy.orm import Session

from app.config import get_db
from app.crud.habit import get_habit
from app.crud.habit_log import (
    create_log,
    update_log,
    get_habit_logs,
    get_log_by_date
)
from app.schemas.habit_log import (
    HabitLogCreate,
    HabitLogUpdate,
    HabitLogResponse
)

router = APIRouter(
    tags=["Habit Logs"]
)


@router.post(
    "/habits/{habit_id}/logs",
    response_model=HabitLogResponse
)
def create_habit_log(
    habit_id: int,
    log: HabitLogCreate,
    db: Session = Depends(get_db)
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

    if log.log_date > date.today():
        raise HTTPException(
            status_code=400,
            detail="Cannot log future date"
        )

    existing_log = get_log_by_date(
        db,
        habit_id,
        log.log_date
    )

    if existing_log:
        raise HTTPException(
            status_code=400,
            detail="Log already exists"
        )

    return create_log(
        db,
        habit_id,
        log
    )


@router.put(
    "/habits/{habit_id}/logs/{log_date}",
    response_model=HabitLogResponse
)
def edit_log(
    habit_id: int,
    log_date: date,
    log: HabitLogUpdate,
    db: Session = Depends(get_db)
):
    updated_log = update_log(
        db,
        habit_id,
        log_date,
        log.completed
    )

    if not updated_log:
        raise HTTPException(
            status_code=404,
            detail="Log not found"
        )

    return updated_log


@router.get(
    "/habits/{habit_id}/logs",
    response_model=list[HabitLogResponse]
)
def get_logs(
    habit_id: int,
    db: Session = Depends(get_db)
):
    return get_habit_logs(
        db,
        habit_id
    )