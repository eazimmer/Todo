"""The command-line interface for the program."""
import argparse

parser = argparse.ArgumentParser(
    prog="todo", description="Track and manage tasks.",
    usage="todo [OPTIONS] COMMAND"
)

subparsers = parser.add_subparsers(title="Commands", dest="command")

list_parser = subparsers.add_parser("list", help="List all tasks.")

add_parser = subparsers.add_parser("add", help="Add a task.")
add_parser.add_argument("name", help="The name of the task.")

remove_parser = subparsers.add_parser("delete", help="Delete a task.")
remove_parser.add_argument(
    "id", type=int, help="The ID of the task to delete."
)

check_parser = subparsers.add_parser("check", help="Mark a task as completed.")
check_parser.add_argument(
    "id", type=int, help="The ID of the task to mark as completed."
)
