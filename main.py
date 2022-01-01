#!/usr/bin/python3

import argparse

from interpreter import Interpreter, InterpretError
from parser import Parser
from printer import Printer
from scanner import Scanner

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
    parser = Parser(tokens)
    expression = parser.parse()
    if expression:
        printer = Printer()
        print(printer.print(expression))
        interpreter = Interpreter()
        print(interpreter.evaluate(expression))


def run_prompt() -> None:
    # TODO: the prompt should report scanning and parsing errors, not swallow/ignore them

    # TODO: the prompt should have a long-lived interpreter to retain state
    while True:
        print('> ', end='')
        command = input()
        if command == '':
            break
        try:
            run(command)
        except InterpretError as e:
            pass


def run_file(filename: str) -> None:
    # TODO: running a file with syntax errors should report all errors
    with open(filename) as f:
        text = f.read()
        try:
            run(text)
        except InterpretError as e:
            exit(70)


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
