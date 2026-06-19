from datetime import date

from fastapi import HTTPException

from app.crud.user import get_user
from app.crud.habit import get_user_habits
from app.crud.habit_log import get_habit_logs
from app.crud.streak import calculate_streak


def get_dashboard_service(
    db,
    user_id
):
    user = get_user(
        db,
        user_id
    )

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

        if any(
            log.log_date == date.today()
            and log.completed
            for log in logs
        ):
            completed_today += 1

        streak = calculate_streak(
            logs
        )

        streaks.append(
            {
                "habitId": habit.id,
                "habitName": habit.name,
                "currentStreak": streak["current_streak"],
                "longestStreak": streak["longest_streak"]
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