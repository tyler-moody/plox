import unittest

from tok import Token, TokenType


class TokenEqTest(unittest.TestCase):
    def test_fails_on_type(self):
        self.assertFalse(
            Token(TokenType.EOF, '', None, 1) == Token(TokenType.WHILE, '', None, 1)
        )

    def test_fails_on_lexeme(self):
        self.assertFalse(
            Token(TokenType.EOF, '', None, 1)
            == Token(TokenType.EOF, 'difference', None, 1)
        )

    def test_fails_on_literal(self):
        self.assertFalse(
            Token(TokenType.EOF, '', None, 1) == Token(TokenType.EOF, '', 5, 1)
        )

    def test_fails_on_line(self):
        self.assertFalse(
            Token(TokenType.EOF, '', None, 1) == Token(TokenType.EOF, '', None, 5)
        )

    def test_succeeds(self):
        self.assertTrue(
            Token(TokenType.EOF, '', None, 1) == Token(TokenType.EOF, '', None, 1)
        )


class TokenTest(unittest.TestCase):
    def test_str(self):
        t = Token(TokenType.THIS, 'this_lexeme', None, 1)
        self.assertEqual(
            'Token(type=TokenType.THIS, lexeme="this_lexeme", literal=None, line=1)',
            str(t),
        )
