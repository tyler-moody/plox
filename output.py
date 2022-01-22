from typing import Optional
from typing_extensions import Protocol


class Outputter(Protocol):
    def out(self, s: str, end: str = '\n') -> None:
        ...


class StdoutOutputter:
    def out(self, s: str, end: str = '\n') -> None:
        print(s, end=end)


class TestOutputter:
    def __init__(self):
        self.message: Optional[str] = None
        self.previous: Optional[str] = None

    def out(self, s: str, end: str = '\n') -> None:
        self.previous = self.message
        self.message = s
