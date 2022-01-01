import unittest

from typing import Any

from expression import Binary, Grouping, Literal, Unary
from interpreter import InterpretError, Interpreter
from test_error_reporter import TestErrorReporter
from tok import Token, TokenType


class InterpreterTest(unittest.TestCase):
    def setUp(self):
        self.error_reporter = TestErrorReporter()
        self.interpreter = Interpreter(error_reporter=self.error_reporter)

    def test_evaluate_literals(self):
        self.assertEqual(False, self.interpreter.evaluate(Literal(value=False)))
        self.assertEqual(True, self.interpreter.evaluate(Literal(value=True)))
        self.assertEqual(None, self.interpreter.evaluate(Literal(value=None)))
        self.assertEqual(5, self.interpreter.evaluate(Literal(value=5)))
        self.assertEqual('string', self.interpreter.evaluate(Literal(value='string')))

    def test_evaluate_grouping(self):
        self.assertEqual(
            5, self.interpreter.evaluate(Grouping(expression=Literal(value=5)))
        )

    #  _   _ _ __   __ _ _ __ _   _
    # | | | | '_ \ / _` | '__| | | |
    # | |_| | | | | (_| | |  | |_| |
    #  \__,_|_| |_|\__,_|_|   \__, |
    #                         |___/
    #  FIGLET: unary
    #

    def test_evaluate_unary(self):
        self.assertEqual(
            -5,
            self.interpreter.evaluate(
                Unary(
                    operator=Token(TokenType.MINUS, '-', None, 1),
                    expression=Literal(value=5.0),
                )
            ),
        )

        self.assertEqual(
            False,
            self.interpreter.evaluate(
                Unary(
                    operator=Token(TokenType.BANG, '!', None, 1),
                    expression=Literal(value=True),
                )
            ),
        )

    def test_evaluate_illegal_unary_op(self):
        with self.assertRaisesRegex(InterpretError, 'Illegal unary operator'):
            self.interpreter.evaluate(
                Unary(
                    operator=Token(TokenType.PLUS, '+', None, 1),
                    expression=Literal(value=False),
                )
            )

    #  _              _   _     _
    # | |_ _ __ _   _| |_| |__ (_)_ __   ___  ___ ___
    # | __| '__| | | | __| '_ \| | '_ \ / _ \/ __/ __|
    # | |_| |  | |_| | |_| | | | | | | |  __/\__ \__ \
    #  \__|_|   \__,_|\__|_| |_|_|_| |_|\___||___/___/
    #  FIGLET: truthiness
    #

    def test_evaluate_false_is_false(self):
        self.assertEqual(
            True,
            self.interpreter.evaluate(
                Unary(
                    operator=Token(TokenType.BANG, '!', None, 1),
                    expression=Literal(value=False),
                )
            ),
        )

    def test_evaluate_none_is_false(self):
        self.assertEqual(
            True,
            self.interpreter.evaluate(
                Unary(
                    operator=Token(TokenType.BANG, '!', None, 1),
                    expression=Literal(value=None),
                )
            ),
        )

    def test_evaluate_string_is_true(self):
        self.assertEqual(
            False,
            self.interpreter.evaluate(
                Unary(
                    operator=Token(TokenType.BANG, '!', None, 1),
                    expression=Literal(value='foo'),
                )
            ),
        )
        # empty strings are true too
        self.assertEqual(
            False,
            self.interpreter.evaluate(
                Unary(
                    operator=Token(TokenType.BANG, '!', None, 1),
                    expression=Literal(value=''),
                )
            ),
        )

    def test_evaluate_zero_is_false(self):
        self.assertEqual(
            True,
            self.interpreter.evaluate(
                Unary(
                    operator=Token(TokenType.BANG, '!', None, 1),
                    expression=Literal(value=0),
                )
            ),
        )

    def test_evaluate_nonzero_number_is_true(self):
        self.assertEqual(
            False,
            self.interpreter.evaluate(
                Unary(
                    operator=Token(TokenType.BANG, '!', None, 1),
                    expression=Literal(value=5),
                )
            ),
        )

    #  _     _
    # | |__ (_)_ __   __ _ _ __ _   _
    # | '_ \| | '_ \ / _` | '__| | | |
    # | |_) | | | | | (_| | |  | |_| |
    # |_.__/|_|_| |_|\__,_|_|   \__, |
    #                           |___/
    #  FIGLET: binary
    #

    def test_evaluate_mismatched_binary_operands(self):
        with self.assertRaisesRegex(
            InterpretError, 'both operands must be float or str'
        ):
            self.interpreter.evaluate(
                Binary(
                    left=Literal(value=5),
                    operator=Token(TokenType.PLUS, '+', None, 1),
                    right=Literal(value='string'),
                )
            ),

    def test_evaluate_binary_plus(self):
        self.assertEqual(
            5,
            self.interpreter.evaluate(
                Binary(
                    left=Literal(value=2),
                    operator=Token(TokenType.PLUS, '+', None, 1),
                    right=Literal(value=3),
                )
            ),
        )

    def test_evaluate_binary_minus(self):
        self.assertEqual(
            5,
            self.interpreter.evaluate(
                Binary(
                    left=Literal(value=7),
                    operator=Token(TokenType.MINUS, '-', None, 1),
                    right=Literal(value=2),
                )
            ),
        )

    def test_evaluate_binary_multiply(self):
        self.assertEqual(
            35,
            self.interpreter.evaluate(
                Binary(
                    left=Literal(value=7),
                    operator=Token(TokenType.STAR, '*', None, 1),
                    right=Literal(value=5),
                )
            ),
        )

    def test_evaluate_binary_divide(self):
        self.assertEqual(
            5,
            self.interpreter.evaluate(
                Binary(
                    left=Literal(value=35),
                    operator=Token(TokenType.SLASH, '/', None, 1),
                    right=Literal(value=7),
                )
            ),
        )

    def test_evaluate_binary_divide_by_zero(self):
        with self.assertRaisesRegex(InterpretError, 'Division by zero'):
            self.interpreter.evaluate(
                Binary(
                    left=Literal(value=5),
                    operator=Token(TokenType.SLASH, '/', None, 1),
                    right=Literal(value=0),
                )
            )

    def test_evaluate_chained_binary_ops(self):
        self.assertEqual(
            420,
            self.interpreter.evaluate(
                Binary(
                    left=Binary(
                        left=Literal(4),
                        operator=Token(TokenType.STAR, '*', None, 1),
                        right=Literal(100),
                    ),
                    operator=Token(TokenType.PLUS, '+', None, 1),
                    right=Binary(
                        left=Literal(100),
                        operator=Token(TokenType.SLASH, '/', None, 1),
                        right=Literal(5),
                    ),
                )
            ),
        )

    def test_evaluate_string_concatenation_with_plus(self):
        self.assertEqual(
            'helloWorld',
            self.interpreter.evaluate(
                Binary(
                    left=Literal(value='hello'),
                    operator=Token(TokenType.PLUS, '+', None, 1),
                    right=Literal(value='World'),
                )
            ),
        )

    def test_evaluate_less(self):
        self.assertEqual(
            True,
            self.interpreter.evaluate(
                Binary(
                    left=Literal(value=4),
                    operator=Token(TokenType.LESS, '<', None, 1),
                    right=Literal(value=5),
                )
            ),
        )
        self.assertEqual(
            False,
            self.interpreter.evaluate(
                Binary(
                    left=Literal(value=5),
                    operator=Token(TokenType.LESS, '<', None, 1),
                    right=Literal(value=4),
                )
            ),
        )

    def test_evaluate_less_equal(self):
        self.assertEqual(
            True,
            self.interpreter.evaluate(
                Binary(
                    left=Literal(value=5),
                    operator=Token(TokenType.LESS_EQUAL, '<=', None, 1),
                    right=Literal(value=5),
                )
            ),
        )
        self.assertEqual(
            False,
            self.interpreter.evaluate(
                Binary(
                    left=Literal(value=6),
                    operator=Token(TokenType.LESS_EQUAL, '<=', None, 1),
                    right=Literal(value=5),
                )
            ),
        )

    def test_evaluate_greater(self):
        self.assertEqual(
            True,
            self.interpreter.evaluate(
                Binary(
                    left=Literal(value=5),
                    operator=Token(TokenType.GREATER, '>', None, 1),
                    right=Literal(value=4),
                )
            ),
        )
        self.assertEqual(
            False,
            self.interpreter.evaluate(
                Binary(
                    left=Literal(value=4),
                    operator=Token(TokenType.GREATER, '>', None, 1),
                    right=Literal(value=5),
                )
            ),
        )

    def test_evaluate_greater_equal(self):
        self.assertEqual(
            True,
            self.interpreter.evaluate(
                Binary(
                    left=Literal(value=6),
                    operator=Token(TokenType.GREATER_EQUAL, '>=', None, 1),
                    right=Literal(value=5),
                )
            ),
        )
        self.assertEqual(
            False,
            self.interpreter.evaluate(
                Binary(
                    left=Literal(value=4),
                    operator=Token(TokenType.GREATER_EQUAL, '>=', None, 1),
                    right=Literal(value=5),
                )
            ),
        )

    def test_evaluate_bang_equal(self):
        self.assertEqual(
            True,
            self.interpreter.evaluate(
                Binary(
                    left=Literal(value=4),
                    operator=Token(TokenType.BANG_EQUAL, '!=', None, 1),
                    right=Literal(value=5),
                )
            ),
        )

        self.assertEqual(
            False,
            self.interpreter.evaluate(
                Binary(
                    left=Literal(value=5),
                    operator=Token(TokenType.BANG_EQUAL, '!=', None, 1),
                    right=Literal(value=5),
                )
            ),
        )


class EqualityTest(unittest.TestCase):
    def do_test(self, expected: bool, left: Any, right: Any) -> None:
        self.assertEqual(
            expected,
            Interpreter().evaluate(
                Binary(
                    left=Literal(value=left),
                    operator=Token(TokenType.EQUAL_EQUAL, '==', None, 1),
                    right=Literal(value=right),
                )
            ),
        )

    def expect_equal(self, left: Any, right: Any) -> None:
        self.do_test(True, left, right)

    def expect_not_equal(self, left: Any, right: Any) -> None:
        self.do_test(False, left, right)

    def test_equal_numbers(self):
        self.expect_equal(5, 5)

    def test_unequal_numbers(self):
        self.expect_not_equal(4, 5)

    def test_equal_strings(self):
        self.expect_equal('foo', 'foo')

    def test_unequal_strings(self):
        self.expect_not_equal('foo', 'bar')

    def test_none_equals_none(self):
        self.expect_equal(None, None)

    def test_none_never_equal(self):
        self.expect_not_equal(None, False)
        self.expect_not_equal(True, None)
        self.expect_not_equal(None, 1)
        self.expect_not_equal(None, 'foo')


class InEqualityTest(unittest.TestCase):
    def do_test(self, expected: bool, left: Any, right: Any) -> None:
        self.assertEqual(
            expected,
            Interpreter().evaluate(
                Binary(
                    left=Literal(value=left),
                    operator=Token(TokenType.BANG_EQUAL, '!=', None, 1),
                    right=Literal(value=right),
                )
            ),
        )

    def expect_not_equal(self, left: Any, right: Any) -> None:
        self.do_test(expected=True, left=left, right=right)

    def expect_equal(self, left: Any, right: Any) -> None:
        self.do_test(expected=False, left=left, right=right)

    def test_equal_numbers(self):
        self.expect_equal(5, 5)

    def test_unequal_numbers(self):
        self.expect_not_equal(4, 5)

    def test_equal_strings(self):
        self.expect_equal('foo', 'foo')

    def test_unequal_strings(self):
        self.expect_not_equal('foo', 'bar')

    def test_none_equals_none(self):
        self.expect_equal(None, None)

    def test_none_never_equal(self):
        self.expect_not_equal(None, False)
        self.expect_not_equal(True, None)
        self.expect_not_equal(None, 1)
        self.expect_not_equal(None, 'foo')
