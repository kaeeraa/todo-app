from copy import deepcopy
from typing import Any, TypedDict
from platformdirs import user_config_path, user_data_path
from pathlib import Path
from logger import Logger
from json import JSONDecodeError, dump, load
from task import Task

APP_NAME: str = "todo-app"
APP_AUTHOR: str = "kaeeraa"


class TaskDict(TypedDict):
    title: str
    completed: bool


class TasksDict(TypedDict):
    tasks: list[TaskDict]


class Paths:
    CONFIG: Path = user_config_path(APP_NAME, APP_AUTHOR)
    DATA: Path = user_data_path(APP_NAME, APP_AUTHOR)

    STYLE: Path = CONFIG / "style.tcss"
    TASKS: Path = DATA / "tasks.json"


class Tasks:
    def __init__(self) -> None:
        self._logger: Logger = Logger("Data")
        self._file: Path = Paths.TASKS
        self._defaultTemplate: TasksDict = {
            "tasks": [
                {"title": "Test Task1", "completed": False},
                {"title": "Completed task", "completed": True},
            ]
        }

        self._data: TasksDict = deepcopy(self._defaultTemplate)

        self._verifyFile()

    def _verifyFile(self) -> None:
        if self._file.exists():
            return None
        self._file.parent.mkdir(parents=True, exist_ok=True)

        with self._file.open(mode="w") as file:
            dump(self._defaultTemplate, file, indent=2)

    def read(self) -> list[Task]:
        """Read tasks from file and return as list of Task objects"""
        self._verifyFile()

        try:
            with self._file.open("r") as f:
                data: TasksDict = load(f)
            tasksData: list[TaskDict] = data["tasks"]
        except (OSError, JSONDecodeError, KeyError, ValueError):
            self._logger.error("Data file is malformed! Using default tasks.")
            tasksData: list[TaskDict] = deepcopy(self._defaultTemplate).get("tasks")

        widgets: list[Task] = []
        valid: list[TaskDict] = []
        for entry in tasksData:
            title: Any = entry.get("title")
            completed: Any = entry.get("completed")

            if not isinstance(title, str):
                self._logger.error(f"Ignoring entry with bad title: {entry!r}")
                continue
            if not isinstance(completed, bool):
                self._logger.error(f"Ignoring entry with bad completed flag: {entry!r}")
                continue

            widgets.append(Task(goal=title, completed=completed))
            valid.append({"title": title, "completed": completed})

        self._data = {"tasks": valid}
        return widgets

    def save(self) -> None:
        """Save list of Task widgets to file"""
        try:
            with self._file.open("w") as f:
                dump(self._data, f, indent=2)
        except OSError as e:
            self._logger.error(f"Error saving tasks: {e}")

    def add(self, task: TaskDict) -> None:
        self._data["tasks"].append(task)

        return self.save()

    def remove(self, index: int) -> None:
        if not (0 <= index < len(self._data["tasks"])):
            self._logger.error(
                f"Index {index} out of range (0..{len(self._data['tasks'])-1})"
            )
            return

        self._data["tasks"].pop(index)
self.save()
