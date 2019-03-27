"""The main function of the program."""
from todo.cli import parser
from todo.commands import list_tasks, add_task, delete_task, check_task, toggle_tasks_by_completion, list_tasks_via_completion, list_tasks_alphabetically, list_tasks_via_creation, list_tasks_via_id, toggle_tasks_by_imcompletion, list_tasks_with_subtasks
from todo.constants import DEFAULT_LIST_PATH, DEFAULT_LIST_NAME
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
        if args.subtasks:
            list_tasks_with_subtasks()
        if args.completion:
            list_tasks_via_completion()
        elif args.alphabetical:
            list_tasks_alphabetically()
        elif args.created:
            list_tasks_via_creation()
        elif args.id:
            list_tasks_via_id()
        else:
            list_tasks()

    elif args.command == "add":
        add_task(args.name, args.parent)

    elif args.command == "delete":
        delete_task(args.id)

    elif args.command == "check":
        check_task(args.id)

    elif args.command == "toggle":
        if args.completion:
            toggle_tasks_by_completion()
        elif args.incomplete:
            toggle_tasks_by_imcompletion()
        else:
            list_tasks()


if __name__ == "__main__":
    main()