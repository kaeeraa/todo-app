from typing import Optional

from textual.widgets import Checkbox


class Task(Checkbox):
    def __init__(self, goal: str = "", completed: bool = False) -> None:
        super().__init__(label=goal, value=completed)

    def updateTask(
        self, goal: Optional[str] = "", completed: Optional[bool] = None
    ) -> None:
        if goal:
            self.label = goal
        if completed is not None:
            self.value = completed
