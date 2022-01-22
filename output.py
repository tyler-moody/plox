from typing import Optional
from typing_extensions import Protocol


class Outputter(Protocol):
    def out(self, s: str) -> None:
        ...


class StdoutOutputter:
    def out(self, s: str) -> None:
        print(s)


class TestOutputter:
    def __init__(self):
        self.message: Optional[str] = None

    def out(self, s: str) -> None:
        self.message = s
