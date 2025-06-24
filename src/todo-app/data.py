from copy import deepcopy
from typing import Optional, TypedDict
from platformdirs import user_config_path, user_data_path
from pathlib import Path
from logger import Logger
from json import JSONDecodeError, dump, load, loads

APP_NAME: str = "todo-app"
APP_AUTHOR: str = "kaeeraa"


class TaskDict(TypedDict):
    title: str
    completed: bool


class TasksDict(TypedDict):
    tasks: list[TaskDict]


class Paths:
    APP_CONFIG: Path = user_config_path(APP_NAME, APP_AUTHOR)
    APP_DATA: Path = user_data_path(APP_NAME, APP_AUTHOR)

    TCSS: Path = APP_CONFIG / "style.tcss"
    TASKS: Path = APP_DATA / "tasks.json"


class Tasks:
    def __init__(self) -> None:
        self._logger: Logger = Logger("Data")
        self._file: Path = Paths.TASKS
        self._data: TasksDict

        # Hardcoded default
        self._defaultTemplate: TasksDict = {
            "tasks": [
                {"title": "Test Task1", "completed": False},
                {"title": "Completed task", "completed": True},
            ]
        }

        self._verifyFile()

    def _verifyFile(self) -> Optional[str]:
        if self._file.exists():
            return None
        self._file.parent.mkdir(parents=True, exist_ok=True)

        with self._file.open(mode="w") as file:
            dump(self._defaultTemplate, file, indent=2)

        return str(self._file)

    def read(self) -> TasksDict:
        """Read tasks from file and return as list of Task widgets"""
        self._verifyFile()

        try:
            with self._file.open("r") as f:
                data: TasksDict = load(f)
            self._data = data
        except (OSError, JSONDecodeError, KeyError, ValueError):
            self._logger.error("Data file is malformed! Using default tasks.")
            self._data = deepcopy(self._defaultTemplate)

        return self._data.copy()

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

    def remove(self, id: int) -> None:
        if 0 > id > len(self._data):
            self._logger.error(
                f"ID {id} out of range! (total entries {len(self._data)})"
            )

        self._data["tasks"].pop(id)

        return self.save()
