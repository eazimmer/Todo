"""Formatters for formatting tasks."""

import abc
import math
from typing import Collection, Optional

from todo.pipelines import TaskPipeline, PassThroughPipeline
from todo.task import Task


def format_simple_task(task: Task) -> str:
    """Format a single task as a string."""


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

    This formatter shows the task ID, a checkbox indicating whether the task
    has been completed and the name of the task.
    """
    # The number of spaces to pad the task ID in the formatting.
    TASK_ID_PADDING = 4

    # The string to indent each sub-task with.
    SUB_TASK_INDENT = " " * 4

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

    @property
    def _indent(self) -> str:
        return self.SUB_TASK_INDENT * (self._current_depth - 1)

    # TODO: Create decorator for changing current indent.
    def format(self, tasks: Collection[Task]) -> str:
        output = ""

        self._current_depth += 1

        for task in self.pipeline.process(tasks):
            checkbox = "[x]" if task.completed else "[ ]"
            output += (
                    self._indent + f"{checkbox} {task.name} ({task.task_id})\n"
            )

            if self._current_depth < self.max_depth:
                output += self.format(task.children)

        self._current_depth -= 1

        return output


class CompletedTaskFormatter(TaskFormatter):
    """A task formatter that displays each tasks that are completed.

    This formatter shows the task ID, a checkbox indicating whether the task
    has been completed and the name of the task.
    """
    # The number of spaces to pad the task ID in the formatting.
    TASK_ID_PADDING = 5

    def format(self, tasks: Collection[Task]) -> str:
        output = ""
        for task in tasks:
            task_id = "{0:<{1}}".format(task.task_id, self.TASK_ID_PADDING)

            if task.completed == True:
                checkbox = "[X]"
                name = task.name
                output += f"{task_id} {checkbox} {name}\n"

        return output


class UncompletedTaskFormatter(TaskFormatter):
    """A task formatter that displays each tasks that are incomplete.

    This formatter shows the task ID, a checkbox indicating whether the task
    has been completed and the name of the task.
    """
    # The number of spaces to pad the task ID in the formatting.
    TASK_ID_PADDING = 5

    def format(self, tasks: Collection[Task]) -> str:
        output = ""
        for task in tasks:
            task_id = "{0:<{1}}".format(task.task_id, self.TASK_ID_PADDING)

            if task.completed == False:
                checkbox = "[ ]"
                name = task.name
                output += f"{task_id} {checkbox} {name}\n"

        return output


class DescriptiveTaskFormatter(TaskFormatter):
    """A task formatter that displays all tasks with all of their information.

    This formatter shows the task ID, a checkbox showing whether the task has
    been completed, the name of the task, the task's description (it it has
    one), and the task's due date (if it has one).
    """
    # The number of spaces to pad the task ID in the formatting.
    TASK_ID_PADDING = 5

    def format(self, tasks: Collection[Task]) -> str:
        output = ""
        for task in tasks:
            task_id = "{0:<{1}}".format(task.task_id, self.TASK_ID_PADDING)
            checkbox = "[X]" if task.completed else "[ ]"
            name = task.name
            due = task.due
            description = task.description

            # Description and due date
            if task.description is not None and task.due is not None:
                output += f"{task_id} {checkbox} {due} {name}: {description}\n"

            # Description
            elif task.description is not None and task.due is None:
                output += f"{task_id} {checkbox} {name}: {description}\n"

            # Due date
            elif task.description is None and task.due is not None:
                output += f"{task_id} {checkbox} {due} {name}\n"

            # Simple
            else:
                output += f"{task_id} {checkbox} {name}\n"

        return output


class DescriptiveCompletedTaskFormatter(TaskFormatter):
    """A task formatter that displays each tasks that are completed.

    This formatter shows the task ID, a checkbox indicating the task is
    completed, the name of the task, the task's description (it it has one),
    and the task's due date (if it has one).
    """
    # The number of spaces to pad the task ID in the formatting.
    TASK_ID_PADDING = 5

    def format(self, tasks: Collection[Task]) -> str:
        output = ""
        for task in tasks:
            task_id = "{0:<{1}}".format(task.task_id, self.TASK_ID_PADDING)

            if task.completed == True:
                checkbox = "[X]"
                name = task.name
                due = task.due
                description = task.description

                # Description and due date
                if task.description is not None and task.due is not None:
                    output += f"{task_id} {checkbox} {due} {name}: {description}\n"

                # Description
                elif task.description is not None and task.due is None:
                    output += f"{task_id} {checkbox} {name}: {description}\n"

                # Due date
                elif task.description is None and task.due is not None:
                    output += f"{task_id} {checkbox} {due} {name}\n"

                # Simple
                else:
                    output += f"{task_id} {checkbox} {name}\n"

        return output


class DescriptiveUncompletedTaskFormatter(TaskFormatter):
    """A task formatter that displays each tasks that are incomplete.

    This formatter shows the task ID, a checkbox indicating the task is
    uncompleted, the name of the task, the task's description (it it has one),
    and the task's due date (if it has one).
    """
    # The number of spaces to pad the task ID in the formatting.
    TASK_ID_PADDING = 5

    def format(self, tasks: Collection[Task]) -> str:
        output = ""
        for task in tasks:
            task_id = "{0:<{1}}".format(task.task_id, self.TASK_ID_PADDING)

            if task.completed == False:
                checkbox = "[ ]"
                name = task.name
                due = task.due
                description = task.description

                # Description and due date
                if task.description is not None and task.due is not None:
                    output += f"{task_id} {checkbox} {due} {name}: {description}\n"

                # Description
                elif task.description is not None and task.due is None:
                    output += f"{task_id} {checkbox} {name}: {description}\n"

                # Due date
                elif task.description is None and task.due is not None:
                    output += f"{task_id} {checkbox} {due} {name}\n"

                # Simple
                else:
                    output += f"{task_id} {checkbox} {name}\n"

        return output
