from typing import Optional
from platformdirs import user_config_path, user_data_path
from pathlib import Path
from logger import Logger
from json import dump

APP_NAME = "todo-app"
APP_AUTHOR = "kaeeraa"


class Paths(object):
    APP_CONFIG: Path = user_config_path(APP_NAME, APP_AUTHOR)
    APP_DATA: Path = user_data_path(APP_NAME, APP_AUTHOR)

    TCSS: Path = Path(APP_CONFIG / "style.tcss")
    TASKS: Path = Path(APP_DATA / "tasks.json")


class Tasks(object):
    def __init__(self) -> None:
        self._logger = Logger("Data")
        self._file = Paths.TASKS

        # Hardcoded default
        self.default: dict[str, list[dict[str, str | bool]]] = {
            "tasks": [
                {"title": "Test Task1", "completed": False},
                {"title": "Completed task", "completed": True},
            ]
        }

        self._verify()

    def _verify(self) -> Optional[str]:
        if self._file.exists():
            return
        self._file.parent.mkdir(parents=True, exist_ok=True)

        with self._file.open(mode="w") as file:
            dump(self.default, file, indent=2)

        return str(self._file)
