from dataclasses import dataclass
from typing import TYPE_CHECKING, Union
from typing_extensions import Protocol

from tok import Token
from visitor import Visitor

Value = Union[bool, None, float, str]


class Expression(Protocol):
    def accept(self, visitor: Visitor):
        ...


@dataclass
class Unary(Expression):
    operator: Token
    expression: Expression

    def accept(self, visitor: Visitor):
        return visitor.visit_unary(self)


@dataclass
class Binary(Expression):
    left: Expression
    operator: Token
    right: Expression

    def accept(self, visitor: Visitor):
        return visitor.visit_binary(self)


@dataclass
class Grouping(Expression):
    expression: Expression

    def accept(self, visitor: Visitor):
        return visitor.visit_grouping(self)


@dataclass
class Literal(Expression):
    value: Value

    def accept(self, visitor: Visitor):
        return visitor.visit_literal(self)
