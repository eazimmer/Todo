"""Formatters for formatting tasks."""

import abc
import math
from typing import Collection, Optional

from todo.pipelines import TaskPipeline, PassThroughPipeline
from todo.task import Task

# The string to indent nested levels of tasks with.
INDENT_PREFIX = " " * 4

# The number of columns to wrap text to.
WRAP_WIDTH = 80


class TaskFormatter(abc.ABC):
    """A formatter for formatting a list of tasks.

    The purpose of this abstract base class is to provide a common interface
    for different methods of formatting tasks. We may want to add new ways of
    formatting tasks in the future, and making classes that implement this
    interface allows us to do that without breaking existing code.
    """

    @abc.abstractmethod
    def format(self, tasks: Collection[Task]) -> str:
        """Format the given tasks as a string."""


class SimpleTaskFormatter(TaskFormatter):
    """A task formatter that shows minimal information about each task.

    This formatter shows a checkbox indicating whether the task has been
    completed, the name of the task and the task ID.
    """
    def __init__(
            self, max_depth: Optional[int] = None,
            pipeline: TaskPipeline = PassThroughPipeline()
    ) -> None:
        """Initialize the object.

        Args:
            pipeline: The pipeline to use to sort/filter the tasks.
            max_depth: The maximum number of levels of nested tasks to display.
        """
        self.max_depth: int = max_depth or math.inf
        self.pipeline = pipeline
        self._current_depth: int = 0

    def format(self, tasks: Collection[Task]) -> str:
        output = ""

        self._current_depth += 1

        for task in self.pipeline.process(tasks):
            checkbox = "[x]" if task.completed else "[ ]"
            output += INDENT_PREFIX * (self._current_depth - 1)
            output += f"{checkbox} {task.name} ({task.task_id})\n"

            if self._current_depth < self.max_depth:
                output += self.format(task.children)

        self._current_depth -= 1

        return output


class DetailedTaskFormatter(TaskFormatter):
    """A task formatter that shows detailed information about each task.

    This formatter shows a checkbox indicating whether the task has been
    completed, the name of the task, the task ID, its due date and description.
    """

    def __init__(
            self, max_depth: Optional[int] = None,
            pipeline: TaskPipeline = PassThroughPipeline()
    ) -> None:
        """Initialize the object.

        Args:
            pipeline: The pipeline to use to sort/filter the tasks.
            max_depth: The maximum number of levels of nested tasks to display.
        """
        self.max_depth: int = max_depth or math.inf
        self.pipeline = pipeline
        self._current_depth: int = 0

    def format(self, tasks: Collection[Task]) -> str:
        output = ""

        self._current_depth += 1

        for task in self.pipeline.process(tasks):
            checkbox = "[x]" if task.completed else "[ ]"

            output += INDENT_PREFIX * (self._current_depth - 1)
            output += f"{checkbox} {task.name} ({task.task_id})\n"

            output += INDENT_PREFIX * self._current_depth
            output += f"Due: {task.due}\n"

            output += INDENT_PREFIX * self._current_depth
            output += f"{task.description}\n"

            output += INDENT_PREFIX * self._current_depth
            output += f"{task.priority}\n"

            if self._current_depth < self.max_depth:
                output += self.format(task.children)

        self._current_depth -= 1

        return output


class SingleTaskFormatter(TaskFormatter):
    """A task formatter that shows detailed information about each task.

    This formatter shows a checkbox indicating whether the task has been
    completed, the name of the task, the task ID, its due date and description.
    """

    def __init__(
            self, max_depth: Optional[int] = None,
    ) -> None:
        """Initialize the object.

        Args:
            max_depth: The maximum number of levels of nested tasks to display.
        """
        self.max_depth: int = max_depth or math.inf
        self._current_depth: int = 0

    def format(self, task) -> str:
        output = ""
        self._current_depth += 1

        checkbox = "[x]" if task.completed else "[ ]"

        output += INDENT_PREFIX * (self._current_depth - 1)
        output += f"{checkbox} {task.name} ({task.task_id})\n"

        output += INDENT_PREFIX * self._current_depth
        output += f"Due: {task.due}\n"

        output += INDENT_PREFIX * self._current_depth
        output += f"{task.description}\n"

        self._current_depth -= 1

        return output
