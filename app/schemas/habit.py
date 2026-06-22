from pydantic import BaseModel, Field
from datetime import datetime

class HabitCreate(BaseModel):
    name: str
    target_days_per_week: int = Field(..., ge=1, le=7, description="Target frequency per week")
    user_id: int

class HabitResponse(BaseModel):
    id: int
    name: str
    target_days_per_week: int
    user_id: int
    created_at: datetime

    class Config:
        from_attributes = True
