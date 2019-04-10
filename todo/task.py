"""Classes for representing tasks and task lists."""
import contextlib
import datetime
import itertools
import json
from pathlib import Path
from typing import List, Optional, Dict, Collection, Any, Generator

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
            created: Optional[datetime.datetime] = None,
            parent: Optional[int] = None,
            children: Optional[List["Task"]] = None,
            description: Optional[str] = None, due=None,
            priority: Optional[str] = None,
    ) -> None:
        self.name: str = name
        self.task_id: int = task_id
        self.completed: bool = completed
        self.created: datetime.datetime = created or datetime.datetime.now()
        self.parent: Optional[int] = parent
        self.children: List[Task] = children or []
        self.description: Optional[str] = description
        self.due = due
        self.priority: Optional[str] = priority

    def walk(self) -> Generator["Task", None, None]:
        """Return a generator for iterating the descendants of this task."""
        for child in self.children:
            yield child
            child.walk()

    def __repr__(self) -> str:
        return f"Task(\"{self.name}\")"


class TaskList:
    """A user-defined collection of tasks.

    The tasks are stored in a dictionary that maps each task ID to its task.
    This allows for efficiently getting a task by its ID. To prevent tasks from
    erroneously being added with the wrong ID, the attribute is protected.
    Tasks can be safely added and removed using the methods in this class.

    The dictionary stores maps both tasks and all their sub-tasks.
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
        self._tasks: Dict[int, Task] = {} if tasks is None else {
            task.task_id: task for task in self._walk_tasks(tasks)
        }

    def _walk_tasks(self, tasks: List[Task]) -> Generator[Task, None, None]:
        """Return a generator for iterating tasks and their descendants."""
        for task in tasks:
            yield task
            yield from self._walk_tasks(task.children)

    def _find_id(self) -> int:
        """Find the first unused task ID."""
        for potential_id in itertools.count():
            if potential_id not in self._tasks.keys():
                return potential_id

    @property
    def tasks(self) -> Collection[Task]:
        """A read-only view of the tasks in this task list."""
        # Return only top-level tasks.
        return [task for task in self._tasks.values() if task.parent is None]

    def add_task(
            self, name: str, parent: Optional[int] = None,
            description: Optional[str] = None, due=None, priority: Optional[str] = None
    ) -> None:
        """Add a task to this task list.

        The ID of the task is set to be the lowest ID not currently in use by
        another task in the task list.

        Args:
            name: The name of the task.
            parent: The ID of a task's parent, or None, if the task is
                top-level.
            description: The description of a task.
            due: The due date of a task.
            priority: The priority of the task
        """
        new_task = Task(
            name=name, task_id=self._find_id(), parent=parent,
            description=description, due=due, priority=priority
        )
        self._tasks[new_task.task_id] = new_task

        if parent is not None:
            self.get_task(parent).children.append(new_task)

        print("Created new task: " + new_task.name + " (ID: " + str(new_task.task_id) + ")")

    def remove_task(self, task_id: int) -> Task:
        """Remove the task with the given ID and return it."""
        task = self.get_task(task_id)
        parent_task = self.get_parent(task_id)

        if parent_task is not None:
            parent_task.children.remove(task)
        print("Removed task: " + task.name + " (ID: " + str(task_id) + ")")
        return self._tasks.pop(task_id)

    def get_task(self, task_id: int) -> Task:
        """Return the task in this task list with the given ID."""
        return self._tasks[task_id]

    def get_parent(self, task_id: int) -> Optional[Task]:
        """Return the parent task of the task with the given ID."""
        parent_id = self.get_task(task_id).parent
        return None if parent_id is None else self.get_task(parent_id)

    @classmethod
    def _serialize_task(cls, task: Task) -> Dict[str, Any]:
        """Convert a task to a JSON-compatible dictionary."""
        return {
            "name": task.name,
            "id": task.task_id,
            "completed": task.completed,
            "created": task.created.timestamp(),
            "parent": task.parent,
            "children": [
                cls._serialize_task(sub_task) for sub_task in task.children
            ]
        }

    @classmethod
    def _deserialize_task(cls, json_task: Dict[str, Any]) -> Task:
        """Convert a JSON-compatible dictionary to a task."""
        return Task(
            name=json_task["name"],
            task_id=json_task["id"],
            completed=json_task["completed"],
            created=datetime.datetime.fromtimestamp(json_task["created"]),
            parent=json_task["parent"],
            children=[
                cls._deserialize_task(sub_task)
                for sub_task in json_task["children"]
            ]
        )

    def save(self, path: Path) -> None:
        """Save this task list to the file system.

        Args:
            path: The path of the file to save this task list to.
        """
        json_object = {
            "name": self.name,
            "tasks": [self._serialize_task(task) for task in self.tasks]
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
                cls._deserialize_task(json_task)
                for json_task in json_object["tasks"]
            ]
        )

        try:
            yield task_list
        finally:
            task_list.save(path)
