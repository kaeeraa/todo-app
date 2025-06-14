from typing import Optional
from platformdirs import user_config_path, user_data_path
from pathlib import Path
from logger import Logger

APP_NAME = "todo-app"
APP_AUTHOR = "kaeeraa"


class Paths(object):
    APP_CONFIG: Path = user_config_path(APP_NAME, APP_AUTHOR)
    APP_DATA: Path = user_data_path(APP_NAME, APP_AUTHOR)

    TCSS: Path = Path(APP_CONFIG / "style.tcss")
    TASKS: Path = Path(APP_DATA / "tasks.json")


class Data(object):
    def __init__(self) -> None:
        self._logger = Logger("Data")

    def generatePath(self, path: Path) -> Optional[str]:
        if path.exists():
            return

        self._logger.warning(f"File {path.name} doesn't exists! Creating...")
        path.parent.mkdir(parents=True, exist_ok=True)
        path.touch()

        return str(path)
