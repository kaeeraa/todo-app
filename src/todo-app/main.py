from typing import Optional
from textual.app import App, ComposeResult
from textual.widgets import Footer, Header
from data import Data, Paths
from logger import Logger


class Todo(App[object]):
    @property
    def CSS_PATH(self) -> str | None:  # type: ignore | its designed to override it
        """Return CSS path if file exists, otherwise None."""
        file: Optional[str]

        if not (file := self.data.generatePath(Paths.TCSS)):
            self.logger.warning(f"CSS file not found at: {Paths.TCSS}")

        return file

    def __init__(self) -> None:
        Logger.setDefaultWidget(self)

        self.logger = Logger("App")
        self.data = Data()

        super().__init__()

        # Check for tasks.json
        self.data.generatePath(Paths.TASKS)

    def compose(self) -> ComposeResult:
        yield Header()

        yield Footer()

    def on_mount(self) -> None:
        """On app launch"""
        pass


def run() -> None:
    Todo().run()


if __name__ == "__main__":
    run()
