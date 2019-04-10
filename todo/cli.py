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
list_parser.add_argument(
    "-p", "--priority", choices=["low", "medium", "high"], action="append", default=[],
    help="Filter the tasks based on priority"
)

search_parser = subparsers.add_parser("search", help="Search for a specific task")
search_parser.add_argument("-n", "--name", type=str, dest="name", nargs=1,
                           help="The name of the task to be searched for")
search_parser.add_argument("-i", "--id", type=int,
    help="Add an extra search field based on id", default=None)
search_parser.add_argument("-t", "--tag", dest="tags", type=str, default=[],
                           nargs="+",
                           help="The tags used to search for tasks")

list_detailed_parser = subparsers.add_parser(
    "list_detailed", help="List tasks with additional information.")

list_detailed_parser.add_argument(
    "-l", "--levels", type=int, default=None,
    help="Limit the number of levels of displayed sub-tasks."
)
list_detailed_parser.add_argument(
    "-s", "--sort", choices=["name", "created"], action="append", default=None,
    help="Sort the tasks by this criteria."
)
list_detailed_parser.add_argument(
    "-f", "--filter", choices=["complete", "incomplete"], action="append",
    default=[], help="Filter the tasks by this criteria."
)
list_detailed_parser.add_argument(
    "-p", "--priority", choices=["low", "medium", "high"], action="append", default=[],
    help="Filter the tasks based on priority"
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
    "--priority", help="Give your task a priority number.", default=None
)

add_parser.add_argument("-t", "--tag", dest="tags", type=str,
                        nargs="+", default=None,
                        help="the tags to assign t the task")


remove_parser = subparsers.add_parser("delete", help="Delete a task.")
remove_parser.add_argument(
    "id", type=int, nargs="+", help="The ID(s) of the task(s) to be deleted."
)

check_parser = subparsers.add_parser("check", help="Mark a task as completed.")
check_parser.add_argument(
    "id", type=int, nargs="+",
    help="The ID(s) of the task(s) to be marked as completed."
)

check_parser = subparsers.add_parser("single", help="display a single task.")
check_parser.add_argument(
    "id", type=int, nargs="+",
    help="The ID of the task to be displayed."
)

modify_parser = subparsers.add_parser("modify", help="Modify tasks.")
add_parser.add_argument(
    "id", type=int, help="The ID of the task to modify.")
add_parser.add_argument(
    "--name", help="Modify the name of the task.", default=None)
add_parser.add_argument(
    "-d", "--description", help="Modify the description for a task.",
    default=None)
add_parser.add_argument(
    "--due", help="Modify the due date for a task.", default=None)
add_parser.add_argument(
    "--priority", help="Modify your task's priority number.", default=None)
