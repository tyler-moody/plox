from __future__ import annotations
from typing_extensions import Protocol


class Visitor(Protocol):
    def visit_unary(self, unary: Unary):
        ...

    def visit_binary(self, binary: Binary):
        ...

    def visit_grouping(self, grouping: Grouping):
        ...

    def visit_literal(self, literal: Literal):
        ...

    def visit_expression_statement(self, statement: Expression):
        ...

    def visit_print_statement(self, statement: Print):
        ...
