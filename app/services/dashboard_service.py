from sqlalchemy.orm import Session
from datetime import date
from app.services.user_service import UserService
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
        summaries = []
        today = date.today()
        
        for h in habits:
            logs = crud_log.get_habit_logs_sorted(db, habit_id=h.id)
            total_logs = len(logs)
            completed_logs = sum(1 for log in logs if log.completed)
            
            total_logs_across_all += total_logs
            total_completions_across_all += completed_logs
            
            # Check if logged completed today
            if crud_log.get_log_by_date(db, h.id, today) and crud_log.get_log_by_date(db, h.id, today).completed:
                completed_today += 1
                
            rate = (completed_logs / total_logs * 100.0) if total_logs > 0 else 0.0
            
            current_streak = 0
            for log in reversed(logs):
                if log.completed:
                    current_streak += 1
                else:
                    break
                    
            summaries.append({
                "id": h.id,
                "name": h.name,
                "current_streak": current_streak,
                "completion_rate": round(rate, 2)
            })
            
        consistency = (total_completions_across_all / total_logs_across_all * 100.0) if total_logs_across_all > 0 else 0.0
        
        return {
            "user_id": user_id,
            "total_habits": total_habits,
            "completed_today": completed_today,
            "consistency_score": round(consistency, 2),
            "habits_summary": summaries
        }