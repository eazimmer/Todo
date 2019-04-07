"""The main function of the program."""
from todo.cli import parser
from todo.commands import list_tasks, add_task, delete_task, check_task
from todo.constants import DEFAULT_LIST_PATH, DEFAULT_LIST_NAME
from todo.pipelines import NameSort, CreationTimeSort, CompletionFilter, \
    MultiPipeline
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

        list_tasks(args.levels, MultiPipeline(pipelines))

    elif args.command == "add":
        add_task(args.name, args.parent, args.description, args.due)

    elif args.command == "delete":
        delete_task(args.id)

    elif args.command == "check":
        check_task(args.id)


if __name__ == "__main__":
    main()
