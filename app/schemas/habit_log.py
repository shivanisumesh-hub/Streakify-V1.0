from datetime import date

from pydantic import BaseModel


class HabitLogCreate(BaseModel):
    log_date: date
    completed: bool = True


class HabitLogUpdate(BaseModel):
    completed: bool


class HabitLogResponse(BaseModel):
    id: int
    habit_id: int
    log_date: date
    completed: bool

    model_config = {
        "from_attributes": True
    }