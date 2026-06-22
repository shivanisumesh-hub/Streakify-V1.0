from datetime import date
from typing import List, Optional
from pydantic import BaseModel

class HabitLogCreate(BaseModel):
    completed: bool = True
    log_date: Optional[date] = None

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
    habitName: str
    currentStreak: int
    longestStreak: int

class DashboardResponse(BaseModel):
    totalHabits: int
    activeHabits: int
    completedToday: int
    currentStreaks: List[HabitSummary]
    consistencyScore: float
