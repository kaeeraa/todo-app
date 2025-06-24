from typing import ClassVar, Optional, TypeAlias, Union
from textual.app import App
from textual.widget import Widget
from textual.notifications import SeverityLevel
from weakref import WeakSet

WidgetType: TypeAlias = Union[Widget, App[object]]


class Logger:
    _instances: ClassVar[WeakSet["Logger"]] = WeakSet()
    _default_widget: ClassVar[Optional[WidgetType]] = None

    def __init__(self, name: str, widget: Optional[WidgetType] = None) -> None:
        self.name: str = name
        self.widget: Widget | App[object]

        if widget is not None:
            self.widget = widget
        elif Logger._default_widget is not None:
            self.widget = Logger._default_widget
        else:
            raise ValueError(
                "No widget provided and no default widget set! "
                "Call Logger.setDefaultWidget() first or pass a widget."
            )

        Logger._instances.add(self)

    def __del__(self):
        Logger._instances.discard(self)

    @classmethod
    def setDefaultWidget(cls, widget: WidgetType) -> None:
        cls._default_widget = widget

    def _log(
        self,
        message: str,
        severity: SeverityLevel = "information",
        timeout: float = 5.0,
    ) -> None:
        self.widget.notify(
            message=message,
            title=self.name,
            severity=severity,
            timeout=timeout,
        )

    def info(self, message: str) -> None:
        """Log an info message."""
        self._log(message, "information")

    def warning(self, message: str) -> None:
        """Log a warning message."""
        self._log(message, "warning")

    def error(self, message: str) -> None:
        """Log an error message."""
        self._log(message, "error")
