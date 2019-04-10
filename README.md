# Todo
This is a CLI program for managing to-do lists.

# Usage
To use this program, clone the repository and execute it with `python -m <directory>` on Windows or `python3 -m <directory>` on macOS/Linux.

## Planned Features
- [x] Adding, removing and listing tasks
- [ ] Multiple to-do lists
- [x] Sorting and filtering of tasks
- [x] Searching for tasks
- [x] Sub-tasks
- [x] Descriptions and due dates for tasks
- [ ] Ability to delete/archive completed tasks in bulk
- [x] Priorities for tasks
- [ ] Tags for grouping tasks
- [ ] Reminders
- [ ] Interactive mode

## Files
- `task.py`: Classes for representing tasks and task lists.
- `formatting.py`: Classes for formatting tasks as strings.
- `cli.py`: The command-line interface for the program.
- `commands.py`: A function for each command that can be called at the command line.
- `constants.py`: Constant values to be used program-wide.
- `pipelines.py`: Methods of sorting and filtering tasks.
- `__init__.py`: This is executed when the package is imported.
- `__main__.py`: This is executed when the package is called at the command-line.

## Contributing
This repository follows the [PEP8](https://www.python.org/dev/peps/pep-0008/) style guide and uses
[Google-style](http://google.github.io/styleguide/pyguide.html#38-comments-and-docstrings) docstrings. Type annotations
should be used wherever possible.
