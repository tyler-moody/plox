from dataclasses import dataclass
from typing import List
from typing_extensions import Protocol

from tok import Token


class Expression(Protocol):
    def accept(self, visitor):
        ...


@dataclass
class Unary(Expression):
    operator: Token
    expression: Expression

    def accept(self, visitor):
        return visitor.visit_unary(self)


@dataclass
class Binary(Expression):
    left: Expression
    operator: Token
    right: Expression

    def accept(self, visitor):
        return visitor.visit_binary(self)


@dataclass
class Grouping(Expression):
    expression: Expression

    def accept(self, visitor):
        return visitor.visit_grouping(self)


@dataclass
class Literal(Expression):
    value: object

    def accept(self, visitor):
        return visitor.visit_literal(self)


# __     ___     _ _               _       _             __
# \ \   / (_)___(_) |_ ___  _ __  (_)_ __ | |_ ___ _ __ / _| __ _  ___ ___
#  \ \ / /| / __| | __/ _ \| '__| | | '_ \| __/ _ \ '__| |_ / _` |/ __/ _ \
#   \ V / | \__ \ | || (_) | |    | | | | | ||  __/ |  |  _| (_| | (_|  __/
#    \_/  |_|___/_|\__\___/|_|    |_|_| |_|\__\___|_|  |_|  \__,_|\___\___|
#  FIGLET: Visitor interface
#


class Visitor(Protocol):
    def visit_unary(self, unary: Unary):
        ...

    def visit_binary(self, binary: Binary):
        ...

    def visit_grouping(self, grouping: Grouping):
        ...

    def visit_literal(self, literal: Literal):
        ...


#  ____       _       _
# |  _ \ _ __(_)_ __ | |_ ___ _ __
# | |_) | '__| | '_ \| __/ _ \ '__|
# |  __/| |  | | | | | ||  __/ |
# |_|   |_|  |_|_| |_|\__\___|_|
#  FIGLET: Printer
#
class Printer:
    def _parenthesize(self, name: str, expressions: List[Expression]) -> str:
        string = '('
        string += name
        for expression in expressions:
            string += f' {expression.accept(self)}'
        string += ')'
        return string

    def print(self, expression: Expression) -> str:
        return expression.accept(self)

    def visit_unary(self, unary: Unary):
        return self._parenthesize(unary.operator._lexeme, [unary.expression])

    def visit_binary(self, binary: Binary):
        return self._parenthesize(binary.operator._lexeme, [binary.left, binary.right])

    def visit_grouping(self, grouping: Grouping):
        return self._parenthesize('group', [grouping.expression])

    def visit_literal(self, literal: Literal):
        return str(literal.value)
