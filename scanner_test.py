import unittest

from typing import List, Tuple

from error import ErrorReporter
from scanner import Scanner
from tok import Token, TokenType


class TestErrorReporter(ErrorReporter):
    def __init__(self):
        self._errors = []

    def report(self, line: int, where: int, message: str) -> None:
        self._errors.append((line, where, message))

    def error(self, line: int, message: str) -> None:
        self.report(line, '', message)

    def errors(self) -> List[Tuple[int, str, str]]:
        return self._errors


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

    def test_scan_bang_operators(self):
        text = '!=!'
        expected = [
            Token(TokenType.BANG_EQUAL, '!=', None, 1),
            Token(TokenType.BANG, '!', None, 1),
        ]
        scanner = Scanner(text)
        actual = scanner.tokens()
        self.assertTrue(all(map(lambda x, y: x == y, expected, actual)))

    def test_scan_equal_operators(self):
        text = '==='
        expected = [
            Token(TokenType.EQUAL_EQUAL, '==', None, 1),
            Token(TokenType.EQUAL, '=', None, 1),
        ]
        scanner = Scanner(text)
        actual = scanner.tokens()
        self.assertTrue(all(map(lambda x, y: x == y, expected, actual)))

    def test_scan_lt_operators(self):
        text = '<<='
        expected = [
            Token(TokenType.LESS, '<', None, 1),
            Token(TokenType.LESS_EQUAL, '<=', None, 1),
        ]
        scanner = Scanner(text)
        actual = scanner.tokens()
        self.assertTrue(all(map(lambda x, y: x == y, expected, actual)))

    def test_scan_gt_operators(self):
        text = '>>='
        expected = [
            Token(TokenType.GREATER, '>', None, 1),
            Token(TokenType.GREATER_EQUAL, '>=', None, 1),
        ]
        scanner = Scanner(text)
        actual = scanner.tokens()
        self.assertTrue(all(map(lambda x, y: x == y, expected, actual)))

    def test_scan_slash(self):
        text = '/'
        expected = [Token(TokenType.SLASH, '/', None, 1)]
        scanner = Scanner(text)
        actual = scanner.tokens()
        self.assertTrue(all(map(lambda x, y: x == y, expected, actual)))

    def test_scan_comment(self):
        text = '///'
        expected = [Token(TokenType.EOF, '', None, 1)]
        scanner = Scanner(text)
        actual = scanner.tokens()
        self.assertTrue(all(map(lambda x, y: x == y, expected, actual)))

    def test_scan_whitespace(self):
        text = ' \r\t'
        expected = [Token(TokenType.EOF, '', None, 1)]
        scanner = Scanner(text)
        actual = scanner.tokens()
        self.assertTrue(all(map(lambda x, y: x == y, expected, actual)))

    def test_scan_newline(self):
        text = '\n'
        expected = [Token(TokenType.EOF, '', None, 2)]
        scanner = Scanner(text)
        actual = scanner.tokens()
        self.assertTrue(all(map(lambda x, y: x == y, expected, actual)))

    def test_scan_unexpected_character(self):
        error_reporter = TestErrorReporter()
        scanner = Scanner(text='^', error_reporter=error_reporter)
        scanner.tokens()
        expected = [(1, '', 'Unexpected character "^"')]
        actual = error_reporter.errors()
        self.assertTrue(expected == actual)
