from tok import Token, TokenType

from error import ErrorReporter, StdoutErrorReporter
from typing import List, Optional


class Scanner:
    def __init__(
        self, text: str, error_reporter: ErrorReporter = StdoutErrorReporter()
    ):
        self._text = text
        self._tokens: List[Token] = []
        self._start = 0
        self._current = 0
        self._line = 1
        self._error_reporter = error_reporter

    def tokens(self) -> List[str]:
        while not self.isAtEnd():
            self._start = self._current
            self.scanToken()
        self._tokens.append(Token(TokenType.EOF, '', None, self._line))
        return self._tokens

    def scanToken(self) -> None:
        c = self.advance()
        if c == '(':
            self.addToken(TokenType.LEFT_PAREN)
        elif c == ')':
            self.addToken(TokenType.RIGHT_PAREN)
        elif c == '{':
            self.addToken(TokenType.LEFT_BRACE)
        elif c == '}':
            self.addToken(TokenType.RIGHT_BRACE)
        elif c == ',':
            self.addToken(TokenType.COMMA)
        elif c == '.':
            self.addToken(TokenType.DOT)
        elif c == '-':
            self.addToken(TokenType.MINUS)
        elif c == '+':
            self.addToken(TokenType.PLUS)
        elif c == ';':
            self.addToken(TokenType.SEMICOLON)
        elif c == '*':
            self.addToken(TokenType.STAR)
        elif c == '!':
            if self.match('='):
                self.addToken(TokenType.BANG_EQUAL)
            else:
                self.addToken(TokenType.BANG)
        elif c == '=':
            if self.match('='):
                self.addToken(TokenType.EQUAL_EQUAL)
            else:
                self.addToken(TokenType.EQUAL)
        elif c == '<':
            if self.match('='):
                self.addToken(TokenType.LESS_EQUAL)
            else:
                self.addToken(TokenType.LESS)
        elif c == '>':
            if self.match('='):
                self.addToken(TokenType.GREATER_EQUAL)
            else:
                self.addToken(TokenType.GREATER)
        elif c == '/':
            if self.match('/'):
                # a comment to end of line
                while not self.isAtEnd() and self.peek() != '\n':
                    self.advance()
            else:
                self.addToken(TokenType.SLASH)
        elif c in [' ', '\r', '\t']:
            pass
        elif c == '\n':
            self._line += 1
        elif c == '"':
            self.string()
        else:
            self._error_reporter.error(
                line=self._line,
                message=f'Unexpected character "{c}"',
            )

    def string(self) -> None:
        while self.peek() != '"' and not self.isAtEnd():
            if self.peek() == '\n':
                self._line += 1
            self.advance()

        if self.isAtEnd():
            self._error_reporter.error(line=self._line, message='Unterminatted string')

        # skip past the closing "
        self.advance()
        value = self._text[self._start + 1 : self._current - 1]
        self.addToken(TokenType.STRING, value)

    def peek(self) -> str:
        if self.isAtEnd():
            return '\0'
        return self._text[self._current]

    def match(self, expected: str) -> bool:
        if self.isAtEnd():
            return False
        elif self._text[self._current] != expected:
            return False
        self._current += 1
        return True

    def advance(self) -> Optional[str]:
        if self._current < len(self._text):
            c = self._text[self._current]
            self._current += 1
            return c
        return None

    def addToken(self, tokenType: TokenType, literal: object = None) -> None:
        text = self._text[self._start : self._current]
        self._tokens.append(Token(tokenType, text, literal, self._line))

    def isAtEnd(self) -> bool:
        return self._current >= len(self._text)
