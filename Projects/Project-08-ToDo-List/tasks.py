class Task:
    def __init__(self, title: str):
        self.title = title
        self.completed = False

    def mark_done(self):
        self.completed = True

    def get_details(self) -> str:
        status = "✓" if self.completed else "✗"
        return f"[{status}] {self.title}"


class DeadlineTask(Task):
    def __init__(self, title: str, due_date: str):
        super().__init__(title)
        self.due_date = due_date

    def get_details(self) -> str:
        base_details = super().get_details()
        return f"{base_details} (Due: {self.due_date})"


class TodoList:
    def __init__(self, owner: str):
        self.owner = owner
        self.tasks: list[Task] = []

    def add_task(self, task: Task):
        self.tasks.append(task)