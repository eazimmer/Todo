"""The main function of the program."""
from todo.cli import parser
from todo.commands import list_tasks, list_detailed_tasks, add_task, delete_task, check_task, single_task
from todo.constants import DEFAULT_LIST_PATH, DEFAULT_LIST_NAME
from todo.pipelines import (
    NameSort, CreationTimeSort, CompletionFilter, PriorityFilter, MultiPipeline
)
from todo.task import TaskList


def main():
    """Run the program."""
    # Create the default task list if it doesn't already exist.
    if not DEFAULT_LIST_PATH.exists():
        task_list = TaskList(DEFAULT_LIST_NAME)
        task_list.save(DEFAULT_LIST_PATH)

    # Parse arguments and run the appropriate function based on which command
    # was called.
    args = parser.parse_args()
    if args.command == "list":
        pipelines = []
        if "name" in args.sort:
            pipelines.append(NameSort())
        if "created" in args.sort:
            pipelines.append(CreationTimeSort(reverse=True))
        if "complete" in args.filter:
            pipelines.append(CompletionFilter(completed=True))
        if "incomplete" in args.filter:
            pipelines.append(CompletionFilter(completed=False))
        if "high" in args.priority:
            pipelines.append(PriorityFilter(priority='high'))
        if "medium" in args.priority:
            pipelines.append(PriorityFilter(priority='medium'))
        if "low" in args.priority:
            pipelines.append(PriorityFilter(priority='low'))

        list_tasks(args.levels, MultiPipeline(pipelines))

    elif args.command == "list_detailed":
        pipelines = []
        if "name" in args.sort:
            pipelines.append(NameSort())
        if "created" in args.sort:
            pipelines.append(CreationTimeSort(reverse=True))
        if "complete" in args.filter:
            pipelines.append(CompletionFilter(completed=True))
        if "incomplete" in args.filter:
            pipelines.append(CompletionFilter(completed=False))
        if "high" in args.priority:
            pipelines.append(PriorityFilter(priority='high'))
        if "medium" in args.priority:
            pipelines.append(PriorityFilter(priority='medium'))
        if "low" in args.priority:
            pipelines.append(PriorityFilter(priority='low'))

        list_detailed_tasks(args.levels, MultiPipeline(pipelines))

    elif args.command == "add":
        add_task(args.name, args.parent, args.description, args.due,
                 args.priority, args.tags)

    elif args.command == "search":
        single_task(args.id, args.name)

    elif args.command == "delete":
        for item in args.id:
            delete_task(item)

    elif args.command == "check":
        for item in args.id:
            check_task(item)

    elif args.command == "single":
        for item in args.id:
            single_task(item)


if __name__ == "__main__":
    main()
