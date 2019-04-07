"""A function for each command."""
from typing import Optional

from todo.constants import DEFAULT_LIST_PATH
from todo.formatting import SimpleTaskFormatter
from todo.pipelines import TaskPipeline
from todo.task import TaskList


def list_tasks(levels: Optional[int], pipeline: TaskPipeline) -> None:
    """List all tasks in the console.

    Args:
        levels: The maximum number of levels of nested sub-tasks to display.
            If `None`, there is no limit.
        pipeline: The pipeline used to sort/filter tasks.
    """
    formatter = SimpleTaskFormatter(max_depth=levels, pipeline=pipeline)

    with TaskList.load(DEFAULT_LIST_PATH) as task_list:
        print(formatter.format(task_list.tasks))


def add_task(
        name: str, parent_id: Optional[int], description: Optional[str], due
) -> None:
    """Add a task.

    Args:
        name: The name of the task.
        parent_id: The ID of the task's parent, or None if task is top-level.
        description: The description of the task.
        due: The due date associated with a task.
    """
    with TaskList.load(DEFAULT_LIST_PATH) as task_list:
        task_list.add_task(
            name, parent=parent_id, description=description, due=due
        )


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

        if any(not task.completed for task in task.walk()):
            print("Not all sub-tasks have been completed!")
            return

        task.completed = True
