from tasks import Task, DeadlineTask, TodoList
from storage import save_to_file, load_from_file


def display_tasks(todo_list: TodoList) -> None:
    """Renders the task list to the terminal."""
    print(f"\n--- {todo_list.owner}'s To-Do List ---")
    if not todo_list.tasks:
        print("No tasks found.")
        return

    for index, task in enumerate(todo_list.tasks, start=1):
        print(f"{index}. {task.get_details()}")


def main():
    # 1. Initialize or load existing list
    my_todo = load_from_file("todos.json")
    my_todo.owner = "Asim"

    # 2. Add tasks if list is fresh
    if not my_todo.tasks:
        task1 = Task("Read gRPC documentation")
        task2 = DeadlineTask("Submit project report", due_date="Friday 5 PM")
        task1.mark_done()

        my_todo.add_task(task1)
        my_todo.add_task(task2)

    # 3. Display UI
    display_tasks(my_todo)

    # 4. Save state
    save_to_file(my_todo, "todos.json")
    print("\n[Tasks saved to todos.json]")


if __name__ == "__main__":
    main()