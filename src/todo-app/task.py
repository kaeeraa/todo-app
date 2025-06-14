from enum import Enum
from typing import Optional

from textual.widgets import Checkbox


class Status(Enum):
    IN_PROGRESS = False
    COMPLETED = True


class Task(Checkbox):
    def __init__(self, goal: str = "", status: Status = Status.IN_PROGRESS) -> None:
        self.label: str = goal
        self.value = status.value

    def updateTask(self, goal: str = "", status: Optional[Status] = None) -> None:
        if goal:
            self.label = goal
        if status:
            self.value = status.value
