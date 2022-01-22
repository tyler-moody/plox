from typing import Optional, Sequence
from typing_extensions import Protocol


class Inputter(Protocol):
    def input(self) -> str:
        ...


class StdinInputter:
    def input(self) -> str:
        return input()


class TestInputter:
    def __init__(self, messages: Sequence[str]):
        self.messages = messages
        self.position = 0

    def input(self) -> str:
        if self.position >= len(self.messages):
            raise EOFError
        m = self.messages[self.position]
        self.position += 1
        return m
