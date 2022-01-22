#!/usr/bin/python3

import argparse

from input import Inputter, StdinInputter
from interpreter import Interpreter, InterpretError
from parser import Parser, ParseError
from printer import Printer
from output import Outputter, StdoutOutputter
from scanner import Scanner, ScanError


class Application:
    def __init__(
        self,
        inputter: Inputter = StdinInputter(),
        outputter: Outputter = StdoutOutputter(),
    ):
        self.inputter = inputter
        self.outputter = outputter

    def run_prompt(self) -> None:
        # TODO: support some amount of history / up key

        printer = Printer()
        interpreter = Interpreter(self.outputter)
        while True:
            try:
                self.outputter.out('> ', end='')
                line = self.inputter.input()
                tokens = Scanner(line).tokens()
                statements = Parser(tokens).parse()
                interpreter.interpret(statements)

            except (ScanError, ParseError, InterpretError) as e:
                self.outputter.out(e)
                break
            except EOFError:
                break

    def run_file(self, filename: str) -> None:
        # TODO: running a file with syntax errors should report all errors
        with open(filename) as f:
            text = f.read()
            try:
                tokens = Scanner(text).tokens()
                statements = Parser(tokens).parse()
                interpreter = Interpreter(self.outputter)
                interpreter.interpret(statements)
            except (ScanError, ParseError, InterpretError) as e:
                self.outputter.out(e)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--filename', help='the lox file to interpret')
    return parser.parse_args()


def main(args: argparse.Namespace) -> None:
    application = Application()

    if args.filename:
        application.run_file(args.filename)
    else:
        application.run_prompt()


if __name__ == '__main__':
    main(parse_args())
