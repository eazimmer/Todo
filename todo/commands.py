"""A function for each command."""
from todo.constants import DEFAULT_LIST_PATH
from todo.formatting import SimpleTaskFormatter, CompletedTaskFormatter, UncompletedTaskFormatter, SubtaskFormatter
from todo.task import TaskList


def list_tasks() -> None:
    """List all uncompleted tasks in the console."""
    formatter = SimpleTaskFormatter()

    with TaskList.load(DEFAULT_LIST_PATH) as task_list:
        print(formatter.format(task_list.tasks))


def add_task(name: str, parent_id=None) -> None:
    """Add a task.

    Args:
        name: The name of the task.
        parent_id: The ID of a sub-task's parent, or None if task is top-level.
    """
    with TaskList.load(DEFAULT_LIST_PATH) as task_list:

        # parent-task
        if parent_id is None:
            task_list.add_task(name)

        # sub-task
        elif parent_id is not None:
            task_list.add_task(name, int(parent_id))


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
        all_complete = True

        # parent-task
        if task.parent is None:
            for other_task in task_list.tasks:
                if other_task.parent is not None and other_task.parent == \
                            task.task_id and not other_task.completed:
                    all_complete = False

            if not all_complete:
                print(
                    "At least one sub-tasks is still incomplete. "
                    "Check that first!")
            else:
                task.completed = True

        # sub-task
        else:
            task.completed = True


def toggle_tasks_by_completion() -> None:
    """Toggles list by completed

    Args:
        None
    """
    formatter = CompletedTaskFormatter()

    with TaskList.load(DEFAULT_LIST_PATH) as task_list:
        sorted_task_list = task_list.tasks
        print(formatter.format(sorted_task_list))


def toggle_tasks_by_imcompletion() -> None:
    """Toggles list by incompletion

        Args:
            None
        """
    formatter = UncompletedTaskFormatter()

    with TaskList.load(DEFAULT_LIST_PATH) as task_list:
        sorted_task_list = task_list.tasks
        print(formatter.format(sorted_task_list))


def list_tasks_via_completion() -> None:
    """Sort lists based on completion

    Args:
        None
    """
    formatter = SimpleTaskFormatter()

    with TaskList.load(DEFAULT_LIST_PATH) as task_list:
        sorted_task_list = task_list.tasks
        completed_tasks = []
        uncompleted_tasks = []

        for task in sorted_task_list:
            if task.completed:
                completed_tasks.append(task)
            else:
                uncompleted_tasks.append(task)

        print("Completed Tasks: ")
        print(formatter.format(completed_tasks))
        print("Uncompleted Tasks: ")
        print(formatter.format(uncompleted_tasks))


def list_tasks_alphabetically() -> None:
    """Lists all tasks in alphabetical order

    Args:
         None
    """

    formatter = SimpleTaskFormatter()

    with TaskList.load(DEFAULT_LIST_PATH) as task_list:
        original_task_list = task_list.tasks
        names_in_order = []
        finalized_list = []

        for task in original_task_list:
            names_in_order.append(task.name)

        names_in_order.sort()

        n = range(len(names_in_order))

        for x in n:
            for task in original_task_list:
                if names_in_order[x] == task.name:
                    finalized_list.append(task)

        print(formatter.format(finalized_list))


def list_tasks_via_creation() -> None:
    """List tasks in order of creation

    Args:
         None
    """

    formatter = SimpleTaskFormatter()

    with TaskList.load(DEFAULT_LIST_PATH) as task_list:
        original_task_list = task_list.tasks
        created_in_order = []
        finalized_list = []

        for task in original_task_list:
            created_in_order.append(task.created)

        created_in_order.sort()

        n = range(len(created_in_order))

        for x in n:
            for task in original_task_list:
                if created_in_order[x] == task.created:
                    finalized_list.append(task)

        print(formatter.format(finalized_list))


def list_tasks_via_id() -> None:
    """List tasks in order of task iD

        Args:
             None
        """

    formatter = SimpleTaskFormatter()

    with TaskList.load(DEFAULT_LIST_PATH) as task_list:
        original_task_list = task_list.tasks
        id_in_order = []
        finalized_list = []

        for task in original_task_list:
            id_in_order.append(task.task_id)

        id_in_order.sort()

        n = range(len(id_in_order))

        for x in n:
            for task in original_task_list:
                if id_in_order[x] == task.task_id:
                    finalized_list.append(task)

        print(formatter.format(finalized_list))


def list_tasks_with_subtasks() -> None:
    """List tasks alongside their respective sub-tasks if they have any.

        Args:
             None
        """

    formatter = SubtaskFormatter()

    with TaskList.load(DEFAULT_LIST_PATH) as task_list:
        print(formatter.format(task_list.tasks))
