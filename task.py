from datetime import datetime
from sqlalchemy import create_engine, String, DateTime, Boolean, select, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, sessionmaker


class Base(DeclarativeBase):
    pass


# --- 2. Define the Task Model ---
class Task(Base):
    __tablename__ = "tasks"  # The name of the table in the database
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255))
    due_date: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    is_completed: Mapped[bool] = mapped_column(Boolean, default=False)
    update_time: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    def mark_complete(self):
        self.is_completed = True
        print(f"Task '{self.name}' marked as complete.")

    def mark_incomplete(self):
        self.is_completed = False

    def is_overdue(self):
        return self.due_date < datetime.now() and not self.is_completed

    def __str__(self) -> str:
        status_icon = "[X]" if self.is_completed else "[ ]"
        date_str = self.due_date.strftime("%b %d, %Y at %I:%M %p")
        return f"{status_icon} {self.name} (Due: {date_str})"

    def __repr__(self) -> str:
        return (
            f"Task(id={self.id!r}, name={self.name!r}, completed={self.is_completed!r})"
        )


if __name__ == "__main__":
    engine = create_engine("sqlite:///tasks.db")
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    t = Task(name="Finish hackathon project", due_date=datetime(2025, 11, 9, 12, 0))
    session.add(t)
    session.commit()

    print("--- Created and saved task ---")
    print(t)  # Uses __str__
    print(repr(t))  # Uses __repr__ - notice it now has an id!
    t.mark_complete()
    session.commit()
    print("\n--- Task marked complete ---")
    print(t)
    queried_task = session.get(Task, 1)  # .get() is the fastest way to get by
    if queried_task is None:
        print("Task not found!")
    else:
        print("\n--- Queried task from DB ---")
        print(queried_task)
        print(f"Is it overdue? {queried_task.is_overdue()}")

    session.close()
