import json
from pathlib import Path
from tasks import Task, DeadlineTask, TodoList


def save_to_file(todo_list: TodoList, filepath: str = "todos.json") -> None:
    """Serializes the TodoList into a JSON file."""
    data = {
        "owner": todo_list.owner,
        "tasks": [
            {
                "title": task.title,
                "completed": task.completed,
                "due_date": getattr(task, "due_date", None),
            }
            for task in todo_list.tasks
        ],
    }
    Path(filepath).write_text(json.dumps(data, indent=2), encoding="utf-8")


def load_from_file(filepath: str = "todos.json") -> TodoList:
    """Loads tasks from a JSON file into a TodoList object."""
    path = Path(filepath)
    if not path.exists():
        return TodoList(owner="User")

    raw_data = json.loads(path.read_text(encoding="utf-8"))
    todo_list = TodoList(owner=raw_data.get("owner", "User"))

    for item in raw_data.get("tasks", []):
        due_date = item.get("due_date")
        if due_date:
            task = DeadlineTask(title=item["title"], due_date=due_date)
        else:
            task = Task(title=item["title"])

        if item.get("completed"):
            task.mark_done()

        todo_list.add_task(task)

    return todo_list