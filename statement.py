from dataclasses import dataclass
from typing_extensions import Protocol

import expression
from visitor import Visitor


class Statement(Protocol):
    def accept(self, visitor: Visitor):
        ...


@dataclass
class Expression:
    expression: expression.Expression

    def accept(self, visitor: Visitor):
        return visitor.visit_expression_statement(self)


@dataclass
class Print:
    expression: expression.Expression

    def accept(self, visitor: Visitor):
        return visitor.visit_print_statement(self)


@dataclass
class Variable:
    name: str
    initializer: expression.Expression

    def accept(self, visitor: Visitor):
        return visitor.visit_variable_statement(self)
