from typing import Optional
from textual.widgets import Checkbox


class Task(Checkbox):
    def __init__(self, goal: str = "", completed: bool = False) -> None:
        super().__init__(label=goal, value=completed)

    def updateTask(
        self, goal: Optional[str] = None, completed: Optional[bool] = None
    ) -> None:
        if goal is not None:
            self.label = goal
        if completed is not None:
            self.value = completed
