def report(line: int, where: str, message: str) -> None:
    print(f'line {line} error {where}: {message}')


def error(line: int, message: str) -> None:
    report(line, '', message)
