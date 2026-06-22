from pydantic import BaseModel
from datetime import date
from typing import List

class HabitLogCreate(BaseModel):
    completed: bool = True

class HabitLogUpdate(BaseModel):
    completed: bool

class HabitLogResponse(BaseModel):
    id: int
    habit_id: int
    log_date: date
    completed: bool

    class Config:
        from_attributes = True

class StreakResponse(BaseModel):
    habit_id: int
    current_streak: int
    max_streak: int

class HabitSummary(BaseModel):
    id: int
    name: str
    current_streak: int
    completion_rate: float

class DashboardResponse(BaseModel):
    user_id: int
    total_habits: int
    completed_today: int
    consistency_score: float
    habits_summary: List[HabitSummary]