from datetime import datetime

class Task:
    def __init__(self, name: str, due_date: datetime):
        self.name: str = name
        self.due_date: datetime = due_date
        self.is_completed: bool = False  # New tasks default to incomplete

    def mark_complete(self):
        self.is_completed = True

    def mark_incomplete(self):
        self.is_completed = False

    def is_overdue(self):
        return self.due_date < datetime.now() and not self.is_completed

    # a user-friendly string representation when print is called
    def __str__(self) -> str:  
        status_icon = "[X]" if self.is_completed else "[ ]"
        date_str = self.due_date.strftime("%b %d, %Y at %I:%M %p")
        return f"{status_icon} {self.name} (Due: {date_str})"

    # a developer friendly string representation
    def __repr__(self) -> str: 
        return f"Task(name='{self.name}', due_date={repr(self.due_date)}, completed={self.is_completed})"
    

if __name__ == "__main__":
    # run python3 task.py to see the output of the test cases
    t = Task("test",datetime(2025,11,8,12,15,36))
    print(t)
    t.mark_complete()
    print(t)
