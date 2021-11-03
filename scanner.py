from tok import Token, TokenType

from error import error
from typing import List, Optional


class Scanner:
    def __init__(self, text: str):
        self._text = text
        self._tokens: List[Token] = []
        self._start = 0
        self._current = 0
        self._line = 1

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
        else:
            error(self._line, f'Unexpected character "{c}"')

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
