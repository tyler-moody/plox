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


if __name__ == '__main__':
    unittest.main()
