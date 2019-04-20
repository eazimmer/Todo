import abc
from typing import Iterable

from todo.task import Task


class TaskPipeline(abc.ABC):
    """A method of sorting or filtering tasks."""

    @abc.abstractmethod
    def process(self, tasks: Iterable[Task]) -> Iterable[Task]:
        """Return the sorted or filtered tasks."""


class PassThroughPipeline(TaskPipeline):
    """A pipeline that returns the data unmodified."""

    def process(self, tasks: Iterable[Task]) -> Iterable[Task]:
        return tasks


class MultiPipeline(TaskPipeline):
    """A pipeline that sorts or filters on multiple criteria."""

    def __init__(self, pipelines: Iterable[TaskPipeline]) -> None:
        """Initialize the pipeline.

        Args:
            pipelines: The pipelines to combine to process the tasks.
        """
        self.pipelines = pipelines

    def process(self, tasks: Iterable[Task]) -> Iterable[Task]:
        output = tasks
        for pipeline in self.pipelines:
            output = pipeline.process(output)
        return output


class NameSort(TaskPipeline):
    """A pipeline that sorts tasks alphabetically by name."""

    def __init__(self, reverse: bool = False) -> None:
        """Initialize the pipeline.

        Args:
            reverse: Sort reverse-alphabetically instead of alphabetically.
        """
        self.reverse = reverse

    def process(self, tasks: Iterable[Task]) -> Iterable[Task]:
        return sorted(tasks, key=lambda x: x.name, reverse=self.reverse)


class CreationTimeSort(TaskPipeline):
    """A pipeline that sorts tasks by when they were created."""

    def __init__(self, reverse: bool = False) -> None:
        """Initialize the pipeline.

        Args:
            reverse: Sort from newest to oldest instead of oldest to newest.
        """
        self.reverse = reverse

    def process(self, tasks: Iterable[Task]) -> Iterable[Task]:
        return sorted(tasks, key=lambda x: x.created, reverse=self.reverse)


class CompletionFilter(TaskPipeline):
    """A pipeline that filters tasks by whether they are complete."""

    def __init__(self, completed: bool = False) -> None:
        """Initialize the pipeline.

        Args:
            completed: Return completed tasks if True or incomplete if False.
        """
        self.completed = completed

    def process(self, tasks: Iterable[Task]) -> Iterable[Task]:
        return (task for task in tasks if task.completed == self.completed)


class PriorityFilter(TaskPipeline):
    """A pipeline that filters tasks by their priority."""

    def __init__(self, priority: str = '') -> None:
        """Initialize the pipeline.

        Args:
            priority: Only tasks of this priority are returned.
        """
        self.priority = priority

    def process(self, tasks: Iterable[Task]) -> Iterable[Task]:
        return (task for task in tasks if task.priority == self.priority)
