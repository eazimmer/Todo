# Todo
This is a CLI program for managing to-do lists.

## Usage
To use this program, clone the repository and execute it with `python -m <directory>` on Windows or `python3 -m <directory>` on macOS/Linux.

## Examples
Add a task to the to-do list with a priority of 'high':
```shell
python -m todo add 'Finish homework' --priority 'high'
```

Add a sub-task of the task with the ID 0 and give it a description:
```shell
python -m todo add 'Write paper' -p 0 -d 'Research, outline and create a first draft.'
```

List all tasks with detailed information:
```shell
python -m todo list -i
```

List incomplete tasks with "assignment" in their name and sort them by when they were created:
```shell
python -m todo list -f incomplete -n 'assignment' -s created
```

Mark the task with the ID 6 as completed:
```shell
python -m todo check 6
```

Delete the tasks with the IDs 3, 4 and 5:
```shell
python -m todo delete 3 4 5
```

Change the due date of the task with the ID 9:
```shell
python -m todo modify 9 --due '2019-04-20'
```

Show detailed information about the task with the ID 1:
```shell
python -m todo info 1
```

## Planned Features
- [x] Adding, removing and listing tasks
- [ ] Multiple to-do lists
- [x] Sorting and filtering of tasks
- [x] Searching for tasks
- [x] Sub-tasks
- [x] Descriptions and due dates for tasks
- [x] Ability to delete/archive completed tasks in bulk
- [x] Priorities for tasks
- [x] Tags for grouping tasks
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
