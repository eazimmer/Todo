"""Constants to be used program-wide."""
from pathlib import Path

# The directory where task lists are stored.
TODO_DIRECTORY = Path.home() / ".todo"

# The path of the user's default task list.
DEFAULT_LIST_PATH = TODO_DIRECTORY / "default.json"

# The name of the user's default task list.
DEFAULT_LIST_NAME = "default"
