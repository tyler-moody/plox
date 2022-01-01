import unittest

from scanner import Scanner, ScanError
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

    def test_scan_operators_whitespace_comments(self):
        text = '// this is a comment\n(( )){} //grouping stuff\n!*+-/=<> <= == // operators'
        expected = [
            Token(TokenType.LEFT_PAREN, '(', None, 2),
            Token(TokenType.LEFT_PAREN, '(', None, 2),
            Token(TokenType.RIGHT_PAREN, ')', None, 2),
            Token(TokenType.RIGHT_PAREN, ')', None, 2),
            Token(TokenType.LEFT_BRACE, '{', None, 2),
            Token(TokenType.RIGHT_BRACE, '}', None, 2),
            Token(TokenType.BANG, '!', None, 3),
            Token(TokenType.STAR, '*', None, 3),
            Token(TokenType.PLUS, '+', None, 3),
            Token(TokenType.MINUS, '-', None, 3),
            Token(TokenType.SLASH, '/', None, 3),
            Token(TokenType.EQUAL, '=', None, 3),
            Token(TokenType.LESS, '<', None, 3),
            Token(TokenType.GREATER, '>', None, 3),
            Token(TokenType.LESS_EQUAL, '<=', None, 3),
            Token(TokenType.EQUAL_EQUAL, '==', None, 3),
        ]
        scanner = Scanner(text)
        actual = scanner.tokens()
        self.assertTrue(all(map(lambda x, y: x == y, expected, actual)))

    def test_scan_string_literal(self):
        text = '"literal"'
        expected = [
            Token(TokenType.STRING, '"literal"', 'literal', 1),
            Token(TokenType.EOF, '', None, 1),
        ]
        scanner = Scanner(text)
        actual = scanner.tokens()
        self.assertTrue(all(map(lambda x, y: x == y, expected, actual)))

    def test_scan_unterminated_string(self):
        with self.assertRaisesRegex(ScanError, 'Unterminated string'):
            Scanner('"literal').tokens()

    def test_scan_number_literal(self):
        text = '5 5.5'
        expected = [
            Token(TokenType.NUMBER, '5', 5, 1),
            Token(TokenType.NUMBER, '5.5', 5.5, 1),
            Token(TokenType.EOF, '', None, 1),
        ]
        scanner = Scanner(text)
        actual = scanner.tokens()
        self.assertTrue(all(map(lambda x, y: x == y, expected, actual)))

    def test_scan_identifier(self):
        text = 'orchid with_underscore withCaps withNumber0'
        expected = [
            Token(TokenType.IDENTIFIER, 'orchid', 'orchid', 1),
            Token(TokenType.IDENTIFIER, 'with_underscore', 'with_underscore', 1),
            Token(TokenType.IDENTIFIER, 'withCaps', 'withCaps', 1),
            Token(TokenType.IDENTIFIER, 'withNumber0', 'withNumber0', 1),
            Token(TokenType.EOF, '', None, 1),
        ]
        scanner = Scanner(text)
        actual = scanner.tokens()
        self.assertTrue(all(map(lambda x, y: x == y, expected, actual)))

    def test_scan_reserved_words(self):
        text = 'and class else false for fun if nil or print return super this true var while'
        expected = [
            Token(TokenType.AND, 'and', 'and', 1),
            Token(TokenType.CLASS, 'class', 'class', 1),
            Token(TokenType.ELSE, 'else', 'else', 1),
            Token(TokenType.FALSE, 'false', 'false', 1),
            Token(TokenType.FOR, 'for', 'for', 1),
            Token(TokenType.FUN, 'fun', 'fun', 1),
            Token(TokenType.IF, 'if', 'if', 1),
            Token(TokenType.NIL, 'nil', 'nil', 1),
            Token(TokenType.OR, 'or', 'or', 1),
            Token(TokenType.PRINT, 'print', 'print', 1),
            Token(TokenType.RETURN, 'return', 'return', 1),
            Token(TokenType.SUPER, 'super', 'super', 1),
            Token(TokenType.THIS, 'this', 'this', 1),
            Token(TokenType.TRUE, 'true', 'true', 1),
            Token(TokenType.VAR, 'var', 'var', 1),
            Token(TokenType.WHILE, 'while', 'while', 1),
        ]
        scanner = Scanner(text)
        actual = scanner.tokens()
        self.assertTrue(all(map(lambda x, y: x == y, expected, actual)))

    def test_scan_reserved_words_and_identifiers(self):
        text = 'and andalite class classy else else0 false false_or_true'
        expected = [
            Token(TokenType.AND, 'and', 'and', 1),
            Token(TokenType.IDENTIFIER, 'andalite', 'andalite', 1),
            Token(TokenType.CLASS, 'class', 'class', 1),
            Token(TokenType.IDENTIFIER, 'classy', 'classy', 1),
            Token(TokenType.ELSE, 'else', 'else', 1),
            Token(TokenType.IDENTIFIER, 'else0', 'else0', 1),
            Token(TokenType.FALSE, 'false', 'false', 1),
            Token(TokenType.IDENTIFIER, 'false_or_true', 'false_or_true', 1),
        ]
        scanner = Scanner(text)
        actual = scanner.tokens()
        self.assertTrue(all(map(lambda x, y: x == y, expected, actual)))

    def test_scan_unexpected_character(self):
        with self.assertRaisesRegex(ScanError, 'Unexpected character "\^"'):
            scanner = Scanner(text='^').tokens()
