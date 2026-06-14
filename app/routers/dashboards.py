from datetime import date

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.config import get_db
from app.crud.user import get_user
from app.crud.habit import get_user_habits
from app.crud.habit_log import get_habit_logs
from app.crud.streak import calculate_streak

router = APIRouter(
    tags=["Dashboard"]
)


@router.get("/users/{user_id}/dashboard")
def get_dashboard(
    user_id: int,
    db: Session = Depends(get_db)
):
    user = get_user(db, user_id)

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    habits = get_user_habits(
        db,
        user_id
    )

    total_habits = len(habits)

    completed_today = 0
    streaks = []

    for habit in habits:
        logs = get_habit_logs(
            db,
            habit.id
        )

        today_log = next(
            (
                log for log in logs
                if log.log_date == date.today()
                and log.completed
            ),
            None
        )

        if today_log:
            completed_today += 1

        streak_info = calculate_streak(logs)

        streaks.append(
            {
                "habit_id": habit.id,
                "habit_name": habit.name,
                "current_streak": streak_info["current_streak"]
            }
        )

    consistency_score = 0

    if total_habits > 0:
        consistency_score = round(
            (completed_today / total_habits) * 100,
            2
        )

    return {
        "totalHabits": total_habits,
        "activeHabits": total_habits,
        "completedToday": completed_today,
        "currentStreaks": streaks,
        "consistencyScore": consistency_score
    }