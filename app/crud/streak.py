from app.models.habit_log import HabitLog


def calculate_streak(logs):
    completed_dates = sorted(
        [
            log.log_date
            for log in logs
            if log.completed
        ]
    )

    if not completed_dates:
        return {
            "current_streak": 0,
            "longest_streak": 0
        }

    longest = 1
    current = 1

    for i in range(1, len(completed_dates)):
        diff = (
            completed_dates[i]
            - completed_dates[i - 1]
        ).days

        if diff == 1:
            current += 1
            longest = max(longest, current)
        else:
            current = 1

    return {
        "current_streak": current,
        "longest_streak": longest
    }