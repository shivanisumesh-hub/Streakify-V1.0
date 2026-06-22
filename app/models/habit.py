from sqlalchemy import CheckConstraint, Column, DateTime, ForeignKey, Index, Integer, String, func
from sqlalchemy.orm import relationship
from app.config import Base

class Habit(Base):
    __tablename__ = "habits"
    __table_args__ = (
        CheckConstraint("target_days_per_week BETWEEN 1 AND 7", name="habits_target_days_per_week_check"),
        Index("idx_habits_user", "user_id"),
    )

    id = Column(Integer, primary_key=True)
    name = Column(String(150), nullable=False)
    target_days_per_week = Column(Integer, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE", name="fk_user"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    owner = relationship("User", back_populates="habits")
    logs = relationship("HabitLog", back_populates="habit", cascade="all, delete-orphan")
