from typing import List

from expression import Binary, Expression, Grouping, Literal, Unary

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
        return self._parenthesize(unary.operator.lexeme, [unary.expression])

    def visit_binary(self, binary: Binary):
        return self._parenthesize(binary.operator.lexeme, [binary.left, binary.right])

    def visit_grouping(self, grouping: Grouping):
        return self._parenthesize('group', [grouping.expression])

    def visit_literal(self, literal: Literal):
        return str(literal.value)
