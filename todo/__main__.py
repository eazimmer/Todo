"""The main function of the program."""
from todo.cli import parser
from todo.commands import (
    list_tasks, add_task, delete_task, check_task, modify_task, show_info, remove_all_tasks
)
from todo.constants import DEFAULT_LIST_PATH, DEFAULT_LIST_NAME
from todo.pipelines import (
    NameSort, CreationTimeSort, CompletionFilter, PriorityFilter,
    MultiPipeline,
    NameSearch, DescriptionSearch)
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

        if args.name:
            pipelines.append(NameSearch(names=args.name))

        if args.description:
            pipelines.append(DescriptionSearch(descriptions=args.description))

        list_tasks(
            levels=args.levels, info=args.info,
            pipeline=MultiPipeline(pipelines)
        )

    elif args.command == "add":
        add_task(
            name=args.name, parent_id=args.parent,
            description=args.description, due=args.due,
            priority=args.priority, tags=args.tags
        )

    elif args.command == "delete":
        for item in args.id:
            delete_task(item)

    elif args.command == "check":
        for item in args.id:
            check_task(item)

    elif args.command == "info":
        show_info(args.id)

    elif args.command == "modify":
        modify_task(
            task_id=args.id, name=args.name, description=args.description,
            due=args.due, priority=args.priority, tag=args.tag
        )

    elif args.command == "clear":
        remove_all_tasks()

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
