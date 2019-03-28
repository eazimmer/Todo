"""Classes for representing tasks and task lists."""
import contextlib
import datetime
import itertools
import json
from pathlib import Path
from typing import List, Optional, Dict, Collection

# The string to indent with when formatting JSON.
from todo.constants import TODO_DIRECTORY

JSON_INDENT = "  "


class Task:
    """A task created by the user.

    Args:
        name: The name of this task.
        task_id: The ID of the task.
        completed: Whether this task has been completed.
        created: The time and date at which this task was created. If None,
            this is the current time and date.
        parent: The ID of a task's parent, or None, if the task is top-level.
        description: The description of a task.
        due: The due date of a task.
    """

    def __init__(
            self, name: str, task_id: int, completed: bool = False,
            created: Optional[datetime.datetime] = None, parent=None,
            description=None, due=None) -> None:
        self.name: str = name
        self.task_id: int = task_id
        self.completed: bool = completed
        self.created: datetime.datetime = created or datetime.datetime.now()
        self.parent = parent
        self.description = description
        self.due = due


class TaskList:
    """A user-defined collection of tasks.

    The tasks are stored in a dictionary that maps each task ID to its task.
    This allows for efficiently getting a task by its ID. To prevent tasks from
    erroneously being added with the wrong ID, the attribute is protected.
    Tasks can be safely added and removed using the methods in this class.
    """

    def __init__(self, name: str, tasks: Optional[List[Task]] = None) -> None:
        """Initialize the object.

        Args:
            name: The name of this task list.
            tasks: The initial tasks to add to this task list. If None, there
                are no tasks.

        Throws:
            ValueError: There is a repeating ID in the given tasks.
        """
        self.name: str = name
        self._tasks: Dict[int, Task] = {
            task.task_id: task for task in (tasks or [])
        }

    def _find_id(self) -> int:
        """Find the first unused task ID."""
        for potential_id in itertools.count():
            if potential_id not in self._tasks.keys():
                return potential_id

    @property
    def tasks(self) -> Collection[Task]:
        """A read-only view of the tasks in this task list."""
        return self._tasks.values()

    def add_task(self, name: str, parent=None, description=None, due=None) -> None:
        """Add a task to this task list.

        The ID of the task is set to be the lowest ID not currently in use by
        another task in the task list.

        Args:
            name: The name of the task.
            parent: The ID of a task's parent, or None, if the task is
            top-level.
            description: The description of a task.
            due: The due date of a task.
        """
        # sub-task
        if parent is not None and description is None and due is None:
            new_task = Task(name=name, task_id=self._find_id(),
                            parent=parent)
            self._tasks[new_task.task_id] = new_task

        # description
        elif parent is None and description is not None and due is None:
            new_task = Task(name=name, task_id=self._find_id(),
                            description=description)
            self._tasks[new_task.task_id] = new_task

        # due date
        elif parent is None and description is None and due is not None:
            new_task = Task(name=name, task_id=self._find_id(), due=due)
            self._tasks[new_task.task_id] = new_task

        # sub-task and description
        elif parent is not None and description is not None and due is None:
            new_task = Task(name=name, task_id=self._find_id(), parent=parent,
                            description=description)
            self._tasks[new_task.task_id] = new_task

        # sub-task and due date
        elif parent is not None and description is None and due is not None:
            new_task = Task(name=name, task_id=self._find_id(), parent=parent,
                            due=due)
            self._tasks[new_task.task_id] = new_task

        # description and due date
        elif parent is None and description is not None and due is not None:
            new_task = Task(name=name, task_id=self._find_id(),
                            description=description, due=due)
            self._tasks[new_task.task_id] = new_task

        # sub-task, description, and due date
        elif parent is not None and description is not None and due is not None:
            new_task = Task(name=name, task_id=self._find_id(), parent=parent,
                            description=description, due=due)
            self._tasks[new_task.task_id] = new_task

        # task with no optional flags selected
        else:
            new_task = Task(name=name, task_id=self._find_id())
            self._tasks[new_task.task_id] = new_task

    def remove_task(self, task_id: int) -> Task:
        """Remove the task with the given ID and return it."""
        return self._tasks.pop(task_id)

    def get_task(self, task_id: int) -> Task:
        """Return the task in this task list with the given ID."""
        return self._tasks[task_id]

    def save(self, path: Path) -> None:
        """Save this task list to the file system.

        Args:
            path: The path of the file to save this task list to.
        """
        json_object = {
            "name": self.name,
            "tasks": [
                {
                    "name": task.name,
                    "id": task.task_id,
                    "completed": task.completed,
                    "created": task.created.timestamp(),
                    "parent": task.parent
                }
                for task in self._tasks.values()
            ]
        }

        # Create the parent directory if it doesn't already exist.
        path.parent.mkdir(parents=True, exist_ok=True)

        with path.open("w") as file:
            json.dump(json_object, file, indent=JSON_INDENT)

    @classmethod
    @contextlib.contextmanager
    def load(cls, path: Path) -> "TaskList":
        """Load a task list from the file system.

        This method is a context manager. That means that it can be used in a
        `with` statement to automatically save the task list when you are done
        editing it. This prevents you from accidentally forgetting to save it.
        The following example loads a task list, adds a task to it and
        automatically saves it.

        >>> with TaskList.load(TODO_DIRECTORY / "tasks.json") as task_list:
        >>>     task_list.add_task("Add documentation")

        Args:
            path: The path of the file to load this task list from.
        """
        with path.open() as file:
            json_object = json.load(file)

        task_list = cls(
            name=json_object["name"],
            tasks=[
                Task(
                    name=json_task["name"],
                    task_id=json_task["id"],
                    completed=json_task["completed"],
                    created=datetime.datetime.fromtimestamp(
                        json_task["created"]),
                    parent=json_task["parent"]
                )
                for json_task in json_object["tasks"]
            ]
        )

        try:
            yield task_list
        finally:
            task_list.save(path)
