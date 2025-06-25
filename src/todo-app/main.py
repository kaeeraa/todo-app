from typing import Optional
from textual.app import App, ComposeResult
from textual.containers import VerticalScroll
from textual.widgets import Footer, Header
from data import Tasks, Paths
from logger import Logger
from task import Task


class Todo(App[object]):
    BINDINGS = [
        ("a", "new_task", "Create new task"),
        ("r", "remove_task", "Remove selected task"),
    ]

    @property
    def CSS_PATH(self) -> str | None:  # type: ignore | its designed to override it
        """Return CSS path if file exists, otherwise None."""
        if not Paths.STYLE.exists():
            self.logger.warning(f"CSS file not found at: {Paths.STYLE}")
            return None
        return str(Paths.STYLE)

    def __init__(self) -> None:
        super().__init__()
        Logger.setDefaultWidget(self)
        self.logger = Logger("App")
        self.tasksController = Tasks()

    def compose(self) -> ComposeResult:
        yield Header()
        self.body = VerticalScroll()
        yield self.body
        yield Footer()

    async def on_mount(self) -> None:
        """On app launch"""
        for task in self.tasksController.read():
            await self.body.mount(task)


def run() -> None:
    Todo().run()


if __name__ == "__main__":
    run()
