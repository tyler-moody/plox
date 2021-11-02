#!/usr/bin/python3

import argparse
import enum

#  _____                       _   _                 _ _ _
# | ____|_ __ _ __ ___  _ __  | | | | __ _ _ __   __| | (_)_ __   __ _
# |  _| | '__| '__/ _ \| '__| | |_| |/ _` | '_ \ / _` | | | '_ \ / _` |
# | |___| |  | | | (_) | |    |  _  | (_| | | | | (_| | | | | | | (_| |
# |_____|_|  |_|  \___/|_|    |_| |_|\__,_|_| |_|\__,_|_|_|_| |_|\__, |
#                                                                |___/
#  FIGLET: Error Handling
#
def report(line: int, where: str, message: str) -> None:
    print(f'line {line} error {where}: {message}')


def error(line: int, message: str) -> None:
    return (line, '', message)


class TokenType(enum.Enum):
    LEFT_PAREN = enum.auto()
    RIGHT_PAREN = enum.auto()
    LEFT_BRACE = enum.auto()
    RIGHT_BRACE = enum.auto()

    COMMA = enum.auto()
    DOT = enum.auto()
    MINUS = enum.auto()
    PLUS = enum.auto()
    SEMICOLON = enum.auto()
    SLASH = enum.auto()
    STAR = enum.auto()

    BANG = enum.auto()
    BANG_EQUAL = enum.auto()
    EQUAL = enum.auto()
    EQUAL_EQUAL = enum.auto()
    GREATER = enum.auto()
    GREATER_EQUAL = enum.auto()
    LESS = enum.auto()
    LESS_EQUAL = enum.auto()

    IDENTIFIER = enum.auto()
    STRING = enum.auto()
    NUMBER = enum.auto()

    AND = enum.auto()
    CLASS = enum.auto()
    ELSE = enum.auto()
    FALSE = enum.auto()
    FUN = enum.auto()
    FOR = enum.auto()
    IF = enum.auto()
    NIL = enum.auto()
    OR = enum.auto()
    PRINT = enum.auto()
    RETURN = enum.auto()
    SUPER = enum.auto()
    THIS = enum.auto()
    TRUE = enum.auto()
    VAR = enum.auto()
    WHILE = enum.auto()

    EOF = enum.auto()


class Token:
    def __init__(self, token_type: TokenType, lexeme: str, literal: object, line: int):
        self._type = token_type
        self._lexeme = lexeme
        self._literal = literal
        self._line = line

    def __eq__(self, other) -> bool:
        if not isinstance(other, Token):
            return False
        return (
            self.__class__ == other.__class__
            and self._type == other._type
            and self._lexeme == other._lexeme
            and self._literal == other._literal
            and self._line == other._line
        )


#  __  __       _
# |  \/  | __ _(_)_ __
# | |\/| |/ _` | | '_ \
# | |  | | (_| | | | | |
# |_|  |_|\__,_|_|_| |_|
#  FIGLET: Main
#


def run(text: str) -> None:
    scanner = Scanner(text)
    tokens = scanner.tokens()
    for token in tokens:
        print(token)


def run_prompt() -> None:
    while True:
        print('> ', end='')
        command = input()
        if command == '':
            break
        run(command)


def run_file(filename: str) -> None:
    with open(filename) as f:
        text = f.read()
        run(text)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--filename', help='the lox file to interpret')
    return parser.parse_args()


def main(args: argparse.Namespace) -> None:
    if args.filename:
        run_file(args.filename)
    else:
        run_prompt()


if __name__ == '__main__':
    main(parse_args())
