"""Formatters for formatting tasks."""

import abc
from typing import Collection

from todo.task import Task


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
    TASK_ID_PADDING = 5

    def format(self, tasks: Collection[Task]) -> str:
        output = ""
        for task in tasks:
            task_id = "{0:<{1}}".format(task.task_id, self.TASK_ID_PADDING)
            checkbox = "[X]" if task.completed else "[ ]"
            name = task.name
            output += f"{task_id} {checkbox} {name}\n"

        return output

    def format_with_completed(self, tasks: Collection[Task]) -> str:
        output = ""
        for task in tasks:
            task_id = "{0:<{1}}".format(task.task_id, self.TASK_ID_PADDING)

            if task.completed == True:
                checkbox = "[X]"
                name = task.name
                output += f"{task_id} {checkbox} {name}\n"

        return output

    def format_with_uncompleted(self, tasks: Collection[Task]) -> str:
        output = ""
        for task in tasks:
            task_id = "{0:<{1}}".format(task.task_id, self.TASK_ID_PADDING)

            if task.completed == False:
                checkbox = "[ ]"
                name = task.name
                output += f"{task_id} {checkbox} {name}\n"

        return output

