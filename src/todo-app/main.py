from typing import Optional
from textual.app import App, ComposeResult
from textual.containers import VerticalScroll
from textual.widgets import Footer, Header, Input
from data import TaskDict, Tasks, Paths
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

        self._new_task_input: Optional[Input] = None

    def compose(self) -> ComposeResult:
        yield Header()
        self.body = VerticalScroll()
        yield self.body
        yield Footer()

    async def on_mount(self) -> None:
        """On app launch"""
        for task in self.tasksController.read():
            await self.body.mount(task)

    async def action_new_task(self) -> None:
        if self._new_task_input:
            return

        inputWidget = Input(placeholder="Enter new task title...")
        self._new_task_input = inputWidget
        await self.body.mount(inputWidget)
        self.set_focus(inputWidget)

    async def on_input_submitted(self, event: Input.Submitted) -> None:
        inputWidget: Input = event.input
        title: str = event.value.strip()

        await inputWidget.remove()
        self._new_task_input = None

        if title:
            task = Task(goal=title, completed=False)
            await self.body.mount(task)
            self.tasksController.add(TaskDict(title=title, completed=False))
            self.set_focus(task)

    async def action_remove_task(self) -> None:
        focused = self.focused
        if not isinstance(focused, Task):
            return

        tasks = list(self.body.children)

        try:
            idx = tasks.index(focused)
        except ValueError:
            return

        await focused.remove()
        self.tasksController.remove(idx)

        if tasks := list(self.body.children):
            nextFocus = tasks[min(idx, len(tasks) - 1)]
            self.set_focus(nextFocus)


def run() -> None:
    Todo().run()


if __name__ == "__main__":
    run()
