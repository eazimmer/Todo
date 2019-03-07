"""A function for each command."""
from todo.constants import DEFAULT_LIST_PATH
from todo.formatting import SimpleTaskFormatter
from todo.task import TaskList


def list_tasks() -> None:
    """List all uncompleted tasks in the console."""
    formatter = SimpleTaskFormatter()

    with TaskList.load(DEFAULT_LIST_PATH) as task_list:
        print(formatter.format(task_list.tasks))


def add_task(name: str) -> None:
    """Add a task.

    Args:
        name: The name of the task.
    """
    with TaskList.load(DEFAULT_LIST_PATH) as task_list:
        task_list.add_task(name)


def delete_task(task_id: int) -> None:
    """Delete a task.

    Args:
        task_id: The ID of the task to delete.
    """
    with TaskList.load(DEFAULT_LIST_PATH) as task_list:
        task_list.remove_task(task_id)


def check_task(task_id: int) -> None:
    """Mark a task as completed.

    Args:
        task_id: The ID of the task to mark as completed.
    """
    with TaskList.load(DEFAULT_LIST_PATH) as task_list:
        task = task_list.get_task(task_id)
        task.completed = True
