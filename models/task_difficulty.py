import datetime
from sqlalchemy import Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy.ext.declarative import declarative_base

from .task import Task
from .base import Base


class TaskDifficulty(Base):
    __tablename__ = "task_difficulties"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    # Foreign Key linking back to the Task
    task_id: Mapped[int] = mapped_column(Integer, ForeignKey("tasks.id"), unique=True, nullable=False)

    # The LLM-generated score
    score: Mapped[int] = mapped_column(Integer, nullable=False)
    reasoning: Mapped[str | None] = mapped_column(String, nullable=True)  # The optional reasoning from the LLM

    # Timestamp for when the score was generated/updated
    create_time: Mapped[datetime.datetime] = mapped_column(DateTime, default=datetime.datetime.now(datetime.timezone.utc))

    # Relationship back to the Task
    task: Mapped[Task] = relationship("Task", back_populates="difficulty_record")
