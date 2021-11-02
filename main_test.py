from main import Scanner, Token, TokenType
import unittest


class ScannerTest(unittest.TestCase):
    def test_scan_empty_file(self):
        scanner = Scanner('')
        self.assertEqual([Token(TokenType.EOF, '', None, 1)], scanner.tokens())


if __name__ == '__main__':
    unittest.main()
