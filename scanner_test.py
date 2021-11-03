import unittest

from scanner import Scanner
from tok import Token, TokenType


class ScannerTest(unittest.TestCase):
    def test_scan_empty_file(self):
        scanner = Scanner('')
        expected = [Token(TokenType.EOF, '', None, 1)]
        actual = scanner.tokens()
        self.assertTrue(all(map(lambda x, y: x == y, expected, actual)))

    def test_isAtEnd_empty(self):
        scanner = Scanner('')
        self.assertTrue(scanner.isAtEnd())

    def test_isAtEnd_and_advance(self):
        expected = 'a'
        scanner = Scanner(expected)
        self.assertFalse(scanner.isAtEnd())
        actual = scanner.advance()
        self.assertTrue(scanner.isAtEnd())
        self.assertEqual(expected, actual)

        self.assertEqual(None, scanner.advance())

    def test_scan_single_character_tokens(self):
        text = '(){},.-+;*'
        expected = [
            Token(TokenType.LEFT_PAREN, '(', None, 1),
            Token(TokenType.RIGHT_PAREN, ')', None, 1),
            Token(TokenType.LEFT_BRACE, '{', None, 1),
            Token(TokenType.RIGHT_BRACE, '}', None, 1),
            Token(TokenType.COMMA, ',', None, 1),
            Token(TokenType.DOT, '.', None, 1),
            Token(TokenType.MINUS, '-', None, 1),
            Token(TokenType.PLUS, '+', None, 1),
            Token(TokenType.SEMICOLON, ';', None, 1),
            Token(TokenType.STAR, '*', None, 1),
        ]

        scanner = Scanner(text)
        actual = scanner.tokens()

        self.assertTrue(all(map(lambda x, y: x == y, expected, actual)))

    def test_scan_unexpected_character(self):
        scanner = Scanner('/')
        scanner.tokens()
        # TODO make an error reporting interface, default to printing implementation, inject a test
        # one here, assert that the expected error is reported
        self.assertTrue(False)
