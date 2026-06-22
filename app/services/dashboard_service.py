from sqlalchemy.orm import Session
from datetime import date
from app.services.user_service import UserService
from app.services.streak_service import StreakService
from app.crud import habit as crud_habit
from app.crud import habit_log as crud_log

class DashboardService:
    @staticmethod
    def generate_dashboard(db: Session, user_id: int):
        UserService.get_user(db, user_id)
        habits = crud_habit.get_user_habits(db, user_id)
        
        total_habits = len(habits)
        completed_today = 0
        total_logs_across_all = 0
        total_completions_across_all = 0
        current_streaks = []
        today = date.today()
        
        for h in habits:
            logs = crud_log.get_habit_logs_sorted(db, habit_id=h.id)
            total_logs = len(logs)
            completed_logs = sum(1 for log in logs if log.completed)
            
            total_logs_across_all += total_logs
            total_completions_across_all += completed_logs
            
            # Check if logged completed today
            today_log = crud_log.get_log_by_date(db, h.id, today)
            if today_log and today_log.completed:
                completed_today += 1

            current_streak, longest_streak = StreakService.calculate_from_logs(logs)

            current_streaks.append({
                "habitName": h.name,
                "currentStreak": current_streak,
                "longestStreak": longest_streak
            })
            
        consistency = (total_completions_across_all / total_logs_across_all * 100.0) if total_logs_across_all > 0 else 0.0
        
        return {
            "totalHabits": total_habits,
            "activeHabits": total_habits,
            "completedToday": completed_today,
            "currentStreaks": current_streaks,
            "consistencyScore": round(consistency, 2)
        }
