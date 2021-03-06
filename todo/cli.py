"""The command-line interface for the program."""
import argparse

parser = argparse.ArgumentParser(
    prog="todo", description="Track and manage tasks.",
    usage="todo [OPTIONS] COMMAND",
    formatter_class=argparse.RawTextHelpFormatter
)

subparsers = parser.add_subparsers(title="Commands", dest="command")

list_parser = subparsers.add_parser("list", help="List tasks.")
list_parser.add_argument(
    "-i", "--info", action="store_true",
    help="Show detailed information about each task."
)
list_parser.add_argument(
    "-l", "--levels", type=int, default=None,
    help="Limit the number of levels of displayed sub-tasks."
)
list_parser.add_argument(
    "-s", "--sort", choices=["name", "created"], action="append", default=[],
    help="Sort the tasks by this criteria."
)
list_parser.add_argument(
    "-f", "--filter", choices=["complete", "incomplete"], action="append",
    default=[], help="Filter the tasks by this criteria."
)
list_parser.add_argument(
    "--priority", choices=["low", "medium", "high"], action="append",
    default=[], help="Filter the tasks based on priority"
)
list_parser.add_argument(
    "-n", "--name",
    help="Filter tasks matching this name. This can be passed multiple times.",
    action="append",
    default=[]
)
list_parser.add_argument(
    "-d", "--description",
    help=(
        "Filter tasks matching this description. "
        "This can be passed multiple times."
    ),
    action="append",
    default=[],
)

add_parser = subparsers.add_parser("add", help="Add a task.")
add_parser.add_argument("name", help="The name of the task.")
add_parser.add_argument(
    "-p", "--parent", type=int,
    help="Used when creating sub-task; designates parent task.", default=None
)
add_parser.add_argument(
    "-d", "--description", help="Give your task a description.", default=None
)
add_parser.add_argument(
    "--due", help="Give your task a due date.", default=None
)
add_parser.add_argument(
    "--priority", choices=["low", "medium", "high"],
    help="Give your task a priority number.", default=None
)
add_parser.add_argument(
    "-t", "--tag", dest="tags", type=str, action="append", default=[],
    help="Assign a tag to the task. This can be passed multiple times."
)

remove_parser = subparsers.add_parser("delete", help="Delete a task.")
remove_parser.add_argument(
    "id", type=int, nargs="+", help="The ID(s) of the task(s) to be deleted."
)

check_parser = subparsers.add_parser("check", help="Mark a task as completed.")
check_parser.add_argument(
    "id", type=int, nargs="+",
    help="The ID(s) of the task(s) to be marked as completed."
)

uncheck_parser = subparsers.add_parser("uncheck",
                                       help="Mark a task as uncompleted.")
uncheck_parser.add_argument("id", type=int, nargs="+",
                            help="The ID of the task to mark uncompleted.")

info_parser = subparsers.add_parser(
    "info", help="Display detailed information about individual tasks."
)
info_parser.add_argument(
    "id", type=int, help="The ID of the task to show information for."
)
info_parser.add_argument(
    "children", type=str, choices=["True", "False"], help="Shows all children of the task"
)

modify_parser = subparsers.add_parser("modify", help="Modify tasks.")
modify_parser.add_argument(
    "id", type=int, help="The ID of the task to modify."
)
modify_parser.add_argument(
    "-n", "--name", type=str, help="Modify the name of the task.", default=None
)
modify_parser.add_argument(
    "-d", "--description", type=str, help="Modify the description for a task.",
    default=None
)
modify_parser.add_argument(
    "-t", "--due", type=str, help="Modify the due date for a task.", default=None
)
modify_parser.add_argument(
    "-p", "--priority", choices=["low", "medium", "high"], type=str, help="Modify your task's priority number.",
    default=None
)
modify_parser.add_argument(
    "-a", "--tag", type=str, help="Modify your task's tag.", default=None
)

clear_parser = subparsers.add_parser(
    "clear", help="clear all tasks from the whole list"
)