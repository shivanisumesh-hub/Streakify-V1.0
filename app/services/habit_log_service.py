from datetime import date

from fastapi import HTTPException

from app.crud.habit import get_habit
from app.crud.habit_log import (
    create_log,
    update_log,
    get_habit_logs,
    get_log_by_date
)


def create_habit_log_service(
    db,
    habit_id,
    log
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
            detail="Future dates not allowed"
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


def update_habit_log_service(
    db,
    habit_id,
    log_date,
    completed
):
    log = update_log(
        db,
        habit_id,
        log_date,
        completed
    )

    if not log:
        raise HTTPException(
            status_code=404,
            detail="Log not found"
        )

    return log


def get_logs_service(
    db,
    habit_id
):
    return get_habit_logs(
        db,
        habit_id
    )