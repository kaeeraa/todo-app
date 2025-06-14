from typing import Optional
from textual.app import App, ComposeResult
from textual.containers import VerticalScroll
from textual.widgets import Footer, Header
from data import Tasks, Paths
from logger import Logger


class Todo(App[object]):
    @property
    def CSS_PATH(self) -> str | None:  # type: ignore | its designed to override it
        """Return CSS path if file exists, otherwise None."""
        file: Optional[str]

        if not (file := Paths.TCSS.touch()):
            self.logger.warning(f"CSS file not found at: {Paths.TCSS}")

        return file

    def __init__(self) -> None:
        Logger.setDefaultWidget(self)

        self.logger = Logger("App")
        self.tasks = Tasks()

        super().__init__()

    def compose(self) -> ComposeResult:
        yield Header()
        with VerticalScroll():
            pass
        yield Footer()

    def on_mount(self) -> None:
        """On app launch"""
        pass


def run() -> None:
    Todo().run()


if __name__ == "__main__":
    run()
