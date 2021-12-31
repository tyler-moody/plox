from typing_extensions import Protocol


class ErrorReporter(Protocol):
    def report(self, line: int, where: str, message: str) -> None:
        ...

    def error(self, line: int, message: str) -> None:
        ...


class StdoutErrorReporter:
    def report(self, line: int, where: str, message: str) -> None:
        print(f'line {line} error {where}: {message}')

    def error(self, line: int, message: str) -> None:
        self.report(line, '', message)
