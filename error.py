class ErrorReporter:
    def report(self, line: int, where: int, message: str) -> None:
        raise NotImplementedError

    def error(self, line: int, message: str) -> None:
        raise NotImplementedError


class StdoutErrorReporter(ErrorReporter):
    def report(self, line: int, where: str, message: str) -> None:
        print(f'line {line} error {where}: {message}')

    def error(self, line: int, message: str) -> None:
        self.report(line, '', message)
