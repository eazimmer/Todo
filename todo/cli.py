"""The command-line interface for the program."""
import argparse

parser = argparse.ArgumentParser(
    prog="todo", description="Track and manage tasks.",
    usage="todo [OPTIONS] COMMAND"
)

subparsers = parser.add_subparsers(title="Commands", dest="command")

list_parser = subparsers.add_parser("list", help="List all tasks.")
toggle_completed_parser = subparsers.add_parser("toggle_completed", help="Toggle list by completed")
toggle_via_incompletion_parser = subparsers.add_parser("toggle_incompletion",help="List all tasks based on incompletion")
search_via_completion_parser = subparsers.add_parser("list_completion", help="List all tasks based on completion")
list_via_alphabet_parser = subparsers.add_parser("list_alph",help="List all tasks in alphabetical order")
list_via_created_parser = subparsers.add_parser("list_created",help="List all tasks in the time the tasks were created")
list_via_id = subparsers.add_parser("list_id",help="List all tasks based on order of id")

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
