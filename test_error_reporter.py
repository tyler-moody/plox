from typing import List, Tuple


class TestErrorReporter:
    def __init__(self):
        self._errors = []

    def report(self, line: int, where: str, message: str) -> None:
        self._errors.append((line, where, message))

    def error(self, line: int, message: str) -> None:
        self.report(line, '', message)

    def errors(self) -> List[Tuple[int, str, str]]:
        return self._errors
