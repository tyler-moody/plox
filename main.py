#!/usr/bin/python3

import argparse

from interpreter import Interpreter, InterpretError
from parser import Parser, ParseError
from printer import Printer
from scanner import Scanner, ScanError

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
    # TODO: support some amount of history / up key

    printer = Printer()
    interpreter = Interpreter()
    while True:
        print('> ', end='')
        command = input()
        try:
            tokens = Scanner(command).tokens()
            expression = Parser(tokens).parse()
            print(printer.print(expression))
            print(interpreter.evaluate(expression))

        except (ScanError, ParseError, InterpretError) as e:
            print(e)


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
