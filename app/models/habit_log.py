from sqlalchemy import Boolean, Column, Date, ForeignKey, Index, Integer, UniqueConstraint, func
from sqlalchemy.orm import relationship
from app.config import Base

class HabitLog(Base):
    __tablename__ = "habit_logs"

    id = Column(Integer, primary_key=True)
    habit_id = Column(Integer, ForeignKey("habits.id", ondelete="CASCADE", name="fk_habit"), nullable=False)
    log_date = Column(Date, server_default=func.current_date(), nullable=False)
    completed = Column(Boolean, default=False, nullable=False)

    __table_args__ = (
        UniqueConstraint("habit_id", "log_date", name="unique_habit_per_day"),
        Index("idx_habit_logs_date", "habit_id", "log_date"),
    )

    habit = relationship("Habit", back_populates="logs")
