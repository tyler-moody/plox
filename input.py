from typing import Optional
from typing_extensions import Protocol


class Inputter(Protocol):
    def input(self) -> str:
        ...


class StdinInputter:
    def input(self) -> str:
        return input()


class TestInputter:
    def __init__(self, message: str):
        self.message = message

    def input(self) -> str:
        return self.message
