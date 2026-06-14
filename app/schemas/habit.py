from datetime import datetime

from pydantic import BaseModel, Field


class HabitCreate(BaseModel):
    name: str
    target_days_per_week: int = Field(
        ge=1,
        le=7
    )
    user_id: int


class HabitResponse(BaseModel):
    id: int
    name: str
    target_days_per_week: int
    user_id: int
    created_at: datetime

    model_config = {
        "from_attributes": True
    }