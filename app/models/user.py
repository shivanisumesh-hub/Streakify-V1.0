from sqlalchemy import Column, DateTime, Index, Integer, String, func
from sqlalchemy.orm import relationship
from app.config import Base

class User(Base):
    __tablename__ = "users"
    __table_args__ = (
        Index("idx_users_email", "email"),
    )

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    habits = relationship("Habit", back_populates="owner", cascade="all, delete-orphan")
