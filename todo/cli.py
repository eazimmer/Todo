"""The command-line interface for the program."""
import argparse

parser = argparse.ArgumentParser(
    prog="todo", description="Track and manage tasks.",
    usage="todo [OPTIONS] COMMAND"
)

subparsers = parser.add_subparsers(title="Commands", dest="command")

list_parser = subparsers.add_parser("list", help="List tasks.")
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

remove_parser = subparsers.add_parser("delete", help="Delete a task.")
remove_parser.add_argument(
    "id", type=int, help="The ID of the task to delete."
)

check_parser = subparsers.add_parser("check", help="Mark a task as completed.")
check_parser.add_argument(
    "id", type=int, help="The ID of the task to mark as completed."
)
