from sqlalchemy import (
    Column,
    Integer,
    Boolean,
    Date,
    ForeignKey,
    UniqueConstraint
)

from sqlalchemy.orm import relationship

from app.config import Base


class HabitLog(Base):
    __tablename__ = "habit_logs"

    id = Column(Integer, primary_key=True, index=True)

    habit_id = Column(
        Integer,
        ForeignKey("habits.id", ondelete="CASCADE"),
        nullable=False
    )

    log_date = Column(Date, nullable=False)

    completed = Column(
        Boolean,
        nullable=False,
        default=True
    )

    habit = relationship(
        "Habit",
        back_populates="logs"
    )

    __table_args__ = (
        UniqueConstraint(
            "habit_id",
            "log_date",
            name="unique_habit_log"
        ),
    )