from typing import Union

from error import ErrorReporter, StdoutErrorReporter
from expression import Binary, Expression, Grouping, Literal, Unary, Value
from tok import Token, TokenType


def to_bool(value: Value) -> bool:
    # everything but None and False is considered True
    return value != None and value != False


class InterpretError(Exception):
    pass


class Interpreter:
    def __init__(self, error_reporter: ErrorReporter = StdoutErrorReporter()):
        self._error_reporter = error_reporter

    def evaluate(self, expression: Expression) -> Value:
        return expression.accept(self)

    def _error(self, line: int, message: str) -> InterpretError:
        self._error_reporter.error(line=line, message=message)
        m = f'line {line} {message}'
        return InterpretError(m)

    def _checkNumberOperand(self, operation: Token, operand: Value) -> None:
        if not isinstance(operand, float):
            raise self._error(
                operation.line,
                f'illegal operand for "{operation.lexeme}": must be a number',
            )

    def visit_unary(self, unary: Unary) -> Value:
        value = self.evaluate(unary.expression)
        if unary.operator.token_type == TokenType.MINUS:
            self._checkNumberOperand(unary.operator, value)
            return -value
        elif unary.operator.token_type == TokenType.BANG:
            return not to_bool(value)
        raise self._error(
            unary.operator.line, f'Illegal unary operator "{unary.operator.lexeme}"'
        )

    def visit_binary(self, binary: Binary) -> Value:
        left = self.evaluate(binary.left)
        right = self.evaluate(binary.right)

        # arithmetic
        if binary.operator.token_type == TokenType.MINUS:
            self._checkNumberOperand(binary.operator, left)
            self._checkNumberOperand(binary.operator, right)
            return left - right
        elif binary.operator.token_type == TokenType.PLUS:
            if (isinstance(left, float) and isinstance(right, float)) or (
                isinstance(left, str) and isinstance(right, str)
            ):
                return left + right
            else:
                raise self._error(
                    binary.operator.line,
                    f'illegal operands "{left}" and "{right}" to "+": both operands must be float or str',
                )
        elif binary.operator.token_type == TokenType.STAR:
            self._checkNumberOperand(binary.operator, left)
            self._checkNumberOperand(binary.operator, right)
            return left * right
        elif binary.operator.token_type == TokenType.SLASH:
            self._checkNumberOperand(binary.operator, left)
            self._checkNumberOperand(binary.operator, right)
            if right == 0:
                raise self._error(binary.operator.line, 'Division by zero')
            return left / right
        # comparison
        elif binary.operator.token_type == TokenType.LESS:
            self._checkNumberOperand(binary.operator, left)
            self._checkNumberOperand(binary.operator, right)
            return left < right
        elif binary.operator.token_type == TokenType.LESS_EQUAL:
            self._checkNumberOperand(binary.operator, left)
            self._checkNumberOperand(binary.operator, right)
            return left <= right
        elif binary.operator.token_type == TokenType.GREATER:
            self._checkNumberOperand(binary.operator, left)
            self._checkNumberOperand(binary.operator, right)
            return left > right
        elif binary.operator.token_type == TokenType.GREATER_EQUAL:
            self._checkNumberOperand(binary.operator, left)
            self._checkNumberOperand(binary.operator, right)
            return left >= right
        # equality
        elif binary.operator.token_type == TokenType.BANG_EQUAL:
            return left != right
        elif binary.operator.token_type == TokenType.EQUAL_EQUAL:
            return left == right

        raise self._error(
            binary.operator.line, f'Illegal binary operator "{binary.operator.lexeme}"'
        )

    def visit_grouping(self, grouping: Grouping) -> Value:
        return self.evaluate(grouping.expression)

    def visit_literal(self, literal: Literal) -> Value:
        value = literal.value
        # force all numeric values to float type
        if type(value) in [int, float]:
            return float(value)
        return value
