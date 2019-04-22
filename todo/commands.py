"""A function for each command."""
import datetime
from typing import Optional, List

from todo.constants import DEFAULT_LIST_PATH, DATE_FORMAT
from todo.formatting import SimpleTaskFormatter, DetailedTaskFormatter
from todo.pipelines import TaskPipeline
from todo.task import TaskList


def list_tasks(
        levels: Optional[int], info: bool, pipeline: TaskPipeline
) -> None:
    """List all tasks in the console.

    Args:
        levels: The maximum number of levels of nested sub-tasks to display.
            If `None`, there is no limit.
        info: Show detailed information about each task.
        pipeline: The pipeline used to sort/filter tasks.
    """
    if info:
        formatter = DetailedTaskFormatter(max_depth=levels, pipeline=pipeline)
    else:
        formatter = SimpleTaskFormatter(max_depth=levels, pipeline=pipeline)

    with TaskList.load(DEFAULT_LIST_PATH) as task_list:
        print(formatter.format(task_list.tasks))


def add_task(
        name: str, parent_id: Optional[int], description: Optional[str],
        due: Optional[str], priority: Optional[str], tags: Optional[List[str]]
) -> None:
    """Add a task.

    Args:
        name: The name of the task.
        parent_id: The ID of the task's parent, or None if task is top-level.
        description: The description of the task.
        due: The due date associated with a task.
        priority: The priority associated with a task
        tags: The tags to assign to the task.
    """
    with TaskList.load(DEFAULT_LIST_PATH) as task_list:
        try:
            due_date = (
                None if due is None
                else datetime.datetime.strptime(due, DATE_FORMAT)
            )
        except ValueError:
            print("Error: Due dates must be in YYYY-MM-DD format.")
            return

        task = task_list.add_task(
            name, parent=parent_id, description=description, due=due_date,
            priority=priority, tags=tags
        )

        print(f"Created new task '{task.name}' with ID {task.task_id}.")


def delete_task(task_id: int) -> None:
    """Delete a task.

    Args:
        task_id: The ID of the task to delete.
    """
    try:
        with TaskList.load(DEFAULT_LIST_PATH) as task_list:
            task = task_list.remove_task(task_id)
    except KeyError:
        print(f"There is no task with the ID {task_id}.")

    print(f"Deleted the task '{task.name}'.")


def check_task(task_id: int) -> None:
    """Mark a task as completed.

    Args:
        task_id: The ID of the task to mark as completed.
    """
    try:
        with TaskList.load(DEFAULT_LIST_PATH) as task_list:
            task = task_list.get_task(task_id)

            if any(not task.completed for task in task.walk()):
                print("Not all sub-tasks have been completed!")
                return

            task.completed = True
            print(f"Task '{task.name}' has been completed.")
    except KeyError:
        print(f"There is no task with the ID {task_id}.")


def uncheck_task(task_id: int) -> None:
    """Mark a task as uncompleted.

    Args:
        task_id: The ID of the task to mark as completed.
    """
    try:
        with TaskList.load(DEFAULT_LIST_PATH) as task_list:
            task = task_list.get_task(task_id)
            task.completed = False
            print(f"Task '{task.name}' has been marked incomplete.")
    except KeyError:
        print(f"There is no task with the ID {task_id}.")


def show_info(task_id: int, show_children: Optional[bool]) -> None:
    """Show information about an individual task.

    Args:
        task_id: The ID of the task to show information for.
        show_children: Enter 'True' if you want to show. 'False' to not.
    """
    formatter = DetailedTaskFormatter(max_depth=1)

    try:
        with TaskList.load(DEFAULT_LIST_PATH) as task_list:
            if show_children == False:
                print(formatter.format([task_list.get_task(task_id)], False))
            else:
                print(formatter.format([task_list.get_task(task_id)], True))
    except KeyError:
        print(f"There is no task with the ID {task_id}.")


def modify_task(task_id: int, name: Optional[str], description: Optional[str],
                due, priority: Optional[str], tag: Optional[str]) -> None:
    """Modify a task.

    Args:
        task_id: The ID of the task to delete.
        name: The edited name of a task.
        description: The edited description of a task.
        due: The edited due date of a task.
        priority: The edited priority number of a task.
        tag: The edited tag of a task
    """
    try:
        due_date = (
            None if due is None
            else datetime.datetime.strptime(due, DATE_FORMAT)
        )
    except ValueError:
        print("Error: Due dates must be in YYYY-MM-DD format.")
        return

    try:
        with TaskList.load(DEFAULT_LIST_PATH) as task_list:
            task_list.modify_task(
                task_id=task_id, name=name, description=description,
                due=due_date, priority=priority, tag=tag)
    except KeyError:
        print(f"There is no task with the ID {task_id}.")


def remove_all_tasks()-> None:
    """ This removes all tasks from the task list"""
    with TaskList.load(DEFAULT_LIST_PATH) as task_list:
        task_list.remove_all_tasks()
    print (f" All Tasks have been deleted. ")


