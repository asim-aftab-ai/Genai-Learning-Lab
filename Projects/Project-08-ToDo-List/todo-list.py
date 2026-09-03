# 1. Base Class (Parent Blueprint)
class Task:
    def __init__(self, title: str):
        self.title = title
        self.completed = False

    def mark_done(self):
        self.completed = True

    # Default way to describe a task
    def get_details(self) -> str:
        status = "✓" if self.completed else "✗"
        return f"[{status}] {self.title}"


# 2. Child Class (Inherits from Task)
class DeadlineTask(Task):
    def __init__(self, title: str, due_date: str):
        # super() borrows the title setup and completed status from Task
        super().__init__(title)
        self.due_date = due_date

    # Method Overriding: Replaces the parent's get_details with custom deadline info
    def get_details(self) -> str:
        base_details = super().get_details()
        return f"{base_details} (Due: {self.due_date})"


# 3. Manager Class (Classes Working Together)
class TodoList:
    def __init__(self, owner: str):
        self.owner = owner
        self.tasks: list[Task] = []

    def add_task(self, task: Task):
        self.tasks.append(task)

    def show_all(self):
        print(f"\n--- {self.owner}'s To-Do List ---")
        if not self.tasks:
            print("No tasks found.")
            return

        for index, task in enumerate(self.tasks, start=1):
            # Polymorphism in action: calls the correct get_details automatically
            print(f"{index}. {task.get_details()}")


# --- Execution Example ---
if __name__ == "__main__":
    # Initialize the list manager
    my_todo = TodoList(owner="Asim")

    # Create instances of both parent and child classes
    task1 = Task("Read gRPC documentation")
    task2 = DeadlineTask("Submit project report", due_date="Friday 5 PM")

    # Mark one task as finished
    task1.mark_done()

    # Add both to the manager
    my_todo.add_task(task1)
    my_todo.add_task(task2)

    # Display everything
    my_todo.show_all()