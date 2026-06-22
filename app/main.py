from fastapi import FastAPI
from app import config
from app.models.user import User
from app.models.habit import Habit
from app.models.habit_log import HabitLog
from app.routers import users, habits, habit_logs, streaks, dashboards

# Force database auto-generation sequence from the structured sub-modules
config.Base.metadata.create_all(bind=config.engine)

app = FastAPI(
    title="Streakify MVP Core Backend",
    description="Clean Multi-tier architecture splitting Controllers, Business Rules, Data Storage and Objects."
)

app.include_router(users.router)
app.include_router(habits.router)
app.include_router(habit_logs.router)
app.include_router(streaks.router)
app.include_router(dashboards.router)