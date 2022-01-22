from typing import List, Sequence

from expression import Binary, Expression, Grouping, Literal, Unary
from statement import Print, Statement
from statement import Expression as ExpressionStatement


class Printer:
    def _parenthesize(self, name: str, expressions: List[Expression]) -> str:
        string = '('
        string += name
        for expression in expressions:
            string += f' {expression.accept(self)}'
        string += ')'
        return string

    def print(self, statements: Sequence[Statement]) -> List[str]:
        return [statement.accept(self) for statement in statements]

    def visit_unary(self, unary: Unary) -> str:
        return self._parenthesize(unary.operator.lexeme, [unary.expression])

    def visit_binary(self, binary: Binary) -> str:
        return self._parenthesize(binary.operator.lexeme, [binary.left, binary.right])

    def visit_grouping(self, grouping: Grouping) -> str:
        return self._parenthesize('group', [grouping.expression])

    def visit_literal(self, literal: Literal) -> str:
        return str(literal.value)

    def visit_expression_statement(self, statement: ExpressionStatement) -> str:
        return statement.expression.accept(self)

    def visit_print_statement(self, statement: Print) -> str:
        return statement.expression.accept(self)
