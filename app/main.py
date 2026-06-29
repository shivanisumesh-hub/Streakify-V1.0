from fastapi import FastAPI
from app.config import engine, Base

# 1. CRITICAL STEP: Import all model modules first so columns attach to the Base registry
from app.models import user, habit, habit_log

# 2. Fire the schema table generation AFTER models have registered themselves
Base.metadata.create_all(bind=engine)

# 3. Include your separate operational endpoint routers
from app.routers import users, habits, habit_logs, streaks, dashboards

app = FastAPI(title="Streakify MVP Backend", version="1.0.0")

app.include_router(users.router)
app.include_router(habits.router)
app.include_router(habit_logs.router)
app.include_router(streaks.router)
app.include_router(dashboards.router)

@app.get("/")
def root():
    return {"message": "Welcome to Streakify"}