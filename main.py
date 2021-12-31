#!/usr/bin/python3

import argparse

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
