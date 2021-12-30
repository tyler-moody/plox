from dataclasses import dataclass
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
