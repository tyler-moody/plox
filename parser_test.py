import unittest

from expression import Binary, Grouping, Literal, Unary
from parser import Parser, ParseError
from tok import Token, TokenType


class ParserTest(unittest.TestCase):
    def test_parse_nothing(self):
        with self.assertRaisesRegex(ParseError, 'No tokens to parse'):
            Parser([]).parse()

    def test_parse_eof(self):
        with self.assertRaisesRegex(ParseError, 'Expected expression'):
            Parser([Token(TokenType.EOF, '', None, 1)]).parse()
            parser.parse()

    #             _
    #  _ __  _ __(_)_ __ ___   __ _ _ __ _   _
    # | '_ \| '__| | '_ ` _ \ / _` | '__| | | |
    # | |_) | |  | | | | | | | (_| | |  | |_| |
    # | .__/|_|  |_|_| |_| |_|\__,_|_|   \__, |
    # |_|                                |___/
    #  FIGLET: primary
    #

    def test_parse_false(self):
        tokens = [
            Token(TokenType.FALSE, 'false', '', 1),
            Token(TokenType.EOF, '', None, 1),
        ]
        expected = Literal(value=False)
        self.assertEqual(expected, Parser(tokens).parse())

    def test_parse_true(self):
        tokens = [
            Token(TokenType.TRUE, 'true', '', 1),
            Token(TokenType.EOF, '', None, 1),
        ]
        expected = Literal(value=True)
        self.assertEqual(expected, Parser(tokens).parse())

    def test_parse_nil(self):
        tokens = [
            Token(TokenType.NIL, 'nil', '', 1),
            Token(TokenType.EOF, '', None, 1),
        ]
        expected = Literal(value=None)
        self.assertEqual(expected, Parser(tokens).parse())

    def test_parse_number(self):
        tokens = [
            Token(TokenType.NUMBER, '5', 5, 1),
            Token(TokenType.EOF, '', None, 1),
        ]
        expected = Literal(value=5)
        self.assertEqual(expected, Parser(tokens).parse())

    def test_parse_string(self):
        tokens = [
            Token(TokenType.STRING, 'hello', 'hello', 1),
            Token(TokenType.EOF, '', None, 1),
        ]
        expected = Literal(value='hello')
        self.assertEqual(expected, Parser(tokens).parse())

    def test_parse_grouping(self):
        tokens = [
            Token(TokenType.LEFT_PAREN, '(', None, 1),
            Token(TokenType.NUMBER, '45.67', 45.67, 1),
            Token(TokenType.RIGHT_PAREN, ')', None, 1),
            Token(TokenType.EOF, '', None, 1),
        ]
        expected = Grouping(expression=Literal(value=45.67))
        self.assertEqual(expected, Parser(tokens).parse())

    def test_parse_unmatched_left_paren(self):
        with self.assertRaisesRegex(ParseError, 'Expected "\)" after "\("'):
            Parser(
                tokens=[
                    Token(TokenType.LEFT_PAREN, '(', None, 1),
                    Token(TokenType.NUMBER, '45.67', 45.67, 1),
                    # missing close paren
                    Token(TokenType.EOF, '', None, 1),
                ]
            ).parse()

    #  _   _ _ __   __ _ _ __ _   _
    # | | | | '_ \ / _` | '__| | | |
    # | |_| | | | | (_| | |  | |_| |
    #  \__,_|_| |_|\__,_|_|   \__, |
    #                         |___/
    #  FIGLET: unary
    #

    def test_parse_unary_minus(self):
        tokens = [
            Token(TokenType.MINUS, '-', None, 1),
            Token(TokenType.NUMBER, '5', 5, 1),
            Token(TokenType.EOF, '', None, 1),
        ]
        expected = Unary(
            operator=Token(TokenType.MINUS, '-', None, 1), expression=Literal(value=5)
        )
        self.assertEqual(expected, Parser(tokens).parse())

    def test_parse_unary_not(self):
        tokens = [
            Token(TokenType.BANG, '!', None, 1),
            Token(TokenType.FALSE, 'false', None, 1),
            Token(TokenType.EOF, '', None, 1),
        ]
        expected = Unary(
            operator=Token(TokenType.BANG, '!', None, 1),
            expression=Literal(value=False),
        )
        self.assertEqual(expected, Parser(tokens).parse())

    #                  _ _   _       _ _           _   _
    #  _ __ ___  _   _| | |_(_)_ __ | (_) ___ __ _| |_(_)_   _____
    # | '_ ` _ \| | | | | __| | '_ \| | |/ __/ _` | __| \ \ / / _ \
    # | | | | | | |_| | | |_| | |_) | | | (_| (_| | |_| |\ V /  __/
    # |_| |_| |_|\__,_|_|\__|_| .__/|_|_|\___\__,_|\__|_| \_/ \___|
    #                         |_|
    #  FIGLET: multiplicative
    #

    def test_parse_multiplication(self):
        tokens = [
            Token(TokenType.NUMBER, '4', 4, 1),
            Token(TokenType.STAR, '*', None, 1),
            Token(TokenType.NUMBER, '5', 5, 1),
            Token(TokenType.EOF, '', None, 1),
        ]
        expected = Binary(
            left=Literal(value=4),
            operator=Token(TokenType.STAR, '*', None, 1),
            right=Literal(value=5),
        )
        self.assertEqual(expected, Parser(tokens).parse())

    def test_parse_division(self):
        tokens = [
            Token(TokenType.NUMBER, '20', 20, 1),
            Token(TokenType.SLASH, '/', None, 1),
            Token(TokenType.NUMBER, '4', 4, 1),
            Token(TokenType.EOF, '', None, 1),
        ]
        expected = Binary(
            left=Literal(value=20),
            operator=Token(TokenType.SLASH, '/', None, 1),
            right=Literal(value=4),
        )
        self.assertEqual(expected, Parser(tokens).parse())

    def test_parse_chain_multiplicative(self):
        tokens = [
            Token(TokenType.NUMBER, '4', 4, 1),
            Token(TokenType.STAR, '*', None, 1),
            Token(TokenType.NUMBER, '20', 20, 1),
            Token(TokenType.SLASH, '/', None, 1),
            Token(TokenType.NUMBER, '5', 5, 1),
            Token(TokenType.EOF, '', None, 1),
        ]
        expected = Binary(
            left=Binary(
                left=Literal(4),
                operator=Token(TokenType.STAR, '*', None, 1),
                right=Literal(value=20),
            ),
            operator=Token(TokenType.SLASH, '/', None, 1),
            right=Literal(value=5),
        )
        self.assertEqual(expected, Parser(tokens).parse())

    def test_parse_additive(self):
        tokens = [
            Token(TokenType.NUMBER, '4', 4, 1),
            Token(TokenType.PLUS, '+', None, 1),
            Token(TokenType.NUMBER, '1', 1, 1),
            Token(TokenType.MINUS, '-', None, 1),
            Token(TokenType.NUMBER, '2', 2, 1),
            Token(TokenType.EOF, '', None, 1),
        ]
        expected = Binary(
            left=Binary(
                left=Literal(4),
                operator=Token(TokenType.PLUS, '+', None, 1),
                right=Literal(value=1),
            ),
            operator=Token(TokenType.MINUS, '-', None, 1),
            right=Literal(value=2),
        )
        self.assertEqual(expected, Parser(tokens).parse())

    #                                       _
    #   ___ ___  _ __ ___  _ __   __ _ _ __(_)___  ___  _ __
    #  / __/ _ \| '_ ` _ \| '_ \ / _` | '__| / __|/ _ \| '_ \
    # | (_| (_) | | | | | | |_) | (_| | |  | \__ \ (_) | | | |
    #  \___\___/|_| |_| |_| .__/ \__,_|_|  |_|___/\___/|_| |_|
    #                     |_|
    #  FIGLET: comparison
    #

    def test_parse_less(self):
        tokens = [
            Token(TokenType.NUMBER, '4', 4, 1),
            Token(TokenType.LESS, '<', None, 1),
            Token(TokenType.NUMBER, '5', 5, 1),
            Token(TokenType.EOF, '', None, 1),
        ]
        expected = Binary(
            left=Literal(value=4),
            operator=Token(TokenType.LESS, '<', None, 1),
            right=Literal(value=5),
        )
        self.assertEqual(expected, Parser(tokens).parse())

    def test_parse_less_equal(self):
        tokens = [
            Token(TokenType.NUMBER, '4', 4, 1),
            Token(TokenType.LESS_EQUAL, '<=', None, 1),
            Token(TokenType.NUMBER, '5', 5, 1),
            Token(TokenType.EOF, '', None, 1),
        ]
        expected = Binary(
            left=Literal(value=4),
            operator=Token(TokenType.LESS_EQUAL, '<=', None, 1),
            right=Literal(value=5),
        )
        self.assertEqual(expected, Parser(tokens).parse())

    def test_parse_greater(self):
        tokens = [
            Token(TokenType.NUMBER, '4', 4, 1),
            Token(TokenType.GREATER, '>', None, 1),
            Token(TokenType.NUMBER, '5', 5, 1),
            Token(TokenType.EOF, '', None, 1),
        ]
        expected = Binary(
            left=Literal(value=4),
            operator=Token(TokenType.GREATER, '>', None, 1),
            right=Literal(value=5),
        )
        self.assertEqual(expected, Parser(tokens).parse())

    def test_parse_greater_equal(self):
        tokens = [
            Token(TokenType.NUMBER, '4', 4, 1),
            Token(TokenType.GREATER_EQUAL, '>=', None, 1),
            Token(TokenType.NUMBER, '5', 5, 1),
            Token(TokenType.EOF, '', None, 1),
        ]
        expected = Binary(
            left=Literal(value=4),
            operator=Token(TokenType.GREATER_EQUAL, '>=', None, 1),
            right=Literal(value=5),
        )
        self.assertEqual(expected, Parser(tokens).parse())

    #                         _ _ _
    #   ___  __ _ _   _  __ _| (_) |_ _   _
    #  / _ \/ _` | | | |/ _` | | | __| | | |
    # |  __/ (_| | |_| | (_| | | | |_| |_| |
    #  \___|\__, |\__,_|\__,_|_|_|\__|\__, |
    #          |_|                    |___/
    #  FIGLET: equality
    #

    def test_parse_equal_equal(self):
        tokens = [
            Token(TokenType.NUMBER, '4', 4, 1),
            Token(TokenType.EQUAL_EQUAL, '==', None, 1),
            Token(TokenType.NUMBER, '5', 5, 1),
            Token(TokenType.EOF, '', None, 1),
        ]
        expected = Binary(
            left=Literal(value=4),
            operator=Token(TokenType.EQUAL_EQUAL, '==', None, 1),
            right=Literal(value=5),
        )
        self.assertEqual(expected, Parser(tokens).parse())

    def test_parse_bang_equal(self):
        tokens = [
            Token(TokenType.NUMBER, '4', 4, 1),
            Token(TokenType.BANG_EQUAL, '!=', None, 1),
            Token(TokenType.NUMBER, '5', 5, 1),
            Token(TokenType.EOF, '', None, 1),
        ]
        expected = Binary(
            left=Literal(value=4),
            operator=Token(TokenType.BANG_EQUAL, '!=', None, 1),
            right=Literal(value=5),
        )
        self.assertEqual(expected, Parser(tokens).parse())
