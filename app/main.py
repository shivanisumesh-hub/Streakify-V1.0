from fastapi import FastAPI

from app.routers import (
    users,
    habits,
    habit_logs,
    streaks,
    dashboards
)

app = FastAPI(
    title="Streakify API",
    version="1.0.0"
)

app.include_router(users.router)
app.include_router(habits.router)
app.include_router(habit_logs.router)
app.include_router(streaks.router)
app.include_router(dashboards.router)


@app.get("/")
def root():
    return {
        "message": "Welcome to Streakify API"
    }