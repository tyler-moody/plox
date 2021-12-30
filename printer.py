from typing import List

from expression import Binary, Expression, Grouping, Literal, Unary


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

    def visit_unary(self, unary: Unary) -> str:
        return self._parenthesize(unary.operator.lexeme, [unary.expression])

    def visit_binary(self, binary: Binary) -> str:
        return self._parenthesize(binary.operator.lexeme, [binary.left, binary.right])

    def visit_grouping(self, grouping: Grouping) -> str:
        return self._parenthesize('group', [grouping.expression])

    def visit_literal(self, literal: Literal) -> str:
        return str(literal.value)
