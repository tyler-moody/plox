import unittest

from expression import Binary, Grouping, Literal, Unary
from printer import Printer
from tok import Token, TokenType


class PrinterTest(unittest.TestCase):
    def test_print_literal(self):
        expected = 'literal'
        expression = Literal(value=expected)
        printer = Printer()
        actual = printer.print([expression])
        self.assertEqual([expected], actual)

    def test_print_unary(self):
        expression = Unary(
            operator=Token(TokenType.MINUS, '-', None, 1), expression=Literal(value=123)
        )
        printer = Printer()
        self.assertEqual(['(- 123)'], printer.print([expression]))

    def test_print_grouping(self):
        expression = Grouping(expression=Literal(value=45.67))
        printer = Printer()
        self.assertEqual(['(group 45.67)'], printer.print([expression]))

    def test_print_binary(self):
        left = Unary(
            operator=Token(TokenType.MINUS, '-', None, 1), expression=Literal(value=123)
        )
        operator = Token(TokenType.STAR, '*', None, 1)
        right = Grouping(expression=Literal(value=45.67))
        expression = Binary(left=left, operator=operator, right=right)
        printer = Printer()
        self.assertEqual(['(* (- 123) (group 45.67))'], printer.print([expression]))
