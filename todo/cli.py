"""The command-line interface for the program."""
import argparse

parser = argparse.ArgumentParser(
    prog="todo", description="Track and manage tasks.",
    usage="todo [OPTIONS] COMMAND"
)

subparsers = parser.add_subparsers(title="Commands", dest="command")

list_parser = subparsers.add_parser("list", help="List all tasks.")
list_parser.add_argument("--subtasks", action="store_true", help="List all subtasks from each task")
list_parser.add_argument("--completion", action="store_true", help="Lists the tasks that are complete")
list_parser.add_argument("--alphabetical", action="store_true", help="List all tasks in alphabetical order")
list_parser.add_argument("--created", action="store_true", help="List all tasks in the time the tasks were created")
list_parser.add_argument("--id", action="store_true", help="List all tasks based on order of id")

toggle_parser = subparsers.add_parser("toggle", help="Toggle tasks based on value")
toggle_parser.add_argument("--completion", action="store_true", help="Toggle list by completed")
toggle_parser.add_argument("--incomplete", action="store_true", help="List all tasks based on incompletion")

add_parser = subparsers.add_parser("add", help="Add a task.")
add_parser.add_argument("name", help="The name of the task.")
add_parser.add_argument("-p", "--parent", type=int, help="Used when creating sub-task; designates parent task.", default=None)
add_parser.add_argument("-d", "--description", help="Give your task a description.", default=None)
add_parser.add_argument("--due", help="Give your task a due date.", default=None)

remove_parser = subparsers.add_parser("delete", help="Delete a task.")
remove_parser.add_argument("id", type=int, help="The ID of the task to delete.")

check_parser = subparsers.add_parser("check", help="Mark a task as completed.")
check_parser.add_argument(
    "id", type=int, help="The ID of the task to mark as completed."
)
