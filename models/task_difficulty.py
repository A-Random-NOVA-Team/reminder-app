import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base
from .task import Task


class TaskDifficulty(Base):
    __tablename__ = "task_difficulties"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    # Foreign Key linking back to the Task
    task_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("tasks.id"), unique=True, nullable=False
    )

    # The LLM-generated score
    score: Mapped[int] = mapped_column(Integer, nullable=False)
    reasoning: Mapped[str | None] = mapped_column(
        String, nullable=True
    )  # The optional reasoning from the LLM

    # Timestamp for when the score was generated/updated
    create_time: Mapped[datetime.datetime] = mapped_column(
        DateTime, default=datetime.datetime.now(datetime.UTC)
    )

    # Relationship back to the Task
    task: Mapped[Task] = relationship("Task", back_populates="difficulty_record")
