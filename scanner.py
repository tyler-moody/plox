from tok import Token, TokenType

from typing import List, Optional

RESERVED_WORDS = {
    'and': TokenType.AND,
    'class': TokenType.CLASS,
    'else': TokenType.ELSE,
    'false': TokenType.FALSE,
    'for': TokenType.FOR,
    'fun': TokenType.FUN,
    'if': TokenType.IF,
    'nil': TokenType.NIL,
    'or': TokenType.OR,
    'print': TokenType.PRINT,
    'return': TokenType.RETURN,
    'super': TokenType.SUPER,
    'this': TokenType.THIS,
    'true': TokenType.TRUE,
    'var': TokenType.VAR,
    'while': TokenType.WHILE,
}


class ScanError(Exception):
    pass


class Scanner:
    def __init__(self, text: str):
        self._text = text
        self._tokens: List[Token] = []
        self._start = 0
        self._current = 0
        self._line = 1

    def tokens(self) -> List[Token]:
        while not self.isAtEnd():
            self._start = self._current
            self._scanToken()
        self._tokens.append(Token(TokenType.EOF, '', None, self._line))
        return self._tokens

    def _error(self, message: str) -> ScanError:
        return ScanError(f'{self._line} {message}')

    def _scanToken(self) -> None:
        def match(expected: str) -> bool:
            if self.isAtEnd():
                return False
            elif self._text[self._current] != expected:
                return False
            self._current += 1
            return True

        def peek() -> str:
            if self.isAtEnd():
                return '\0'
            return self._text[self._current]

        def peekNext() -> str:
            if self._current + 1 >= len(self._text):
                return '\0'
            return self._text[self._current + 1]

        def string() -> None:
            while peek() != '"' and not self.isAtEnd():
                if peek() == '\n':
                    self._line += 1
                self.advance()

            if self.isAtEnd():
                raise self._error('Unterminated string')

            # skip past the closing "
            self.advance()
            value = self._text[self._start + 1 : self._current - 1]
            self.addToken(TokenType.STRING, value)

        def isDigit(c: str) -> bool:
            return '0' <= c <= '9'

        def number() -> None:
            while isDigit(peek()):
                self.advance()

            if peek() == '.' and isDigit(peekNext()):
                self.advance()

            while isDigit(peek()):
                self.advance()

            value = float(self._text[self._start : self._current])
            self.addToken(TokenType.NUMBER, value)

        def isAlpha(c: str) -> bool:
            return 'a' <= c <= 'z' or 'A' <= c <= 'Z'

        def isIdentifierCharacter(c: str) -> bool:
            return isDigit(c) or isAlpha(c) or c in ['_']

        def identifier() -> None:
            while isIdentifierCharacter(peek()):
                self.advance()
            text = self._text[self._start : self._current]
            token_type = RESERVED_WORDS.get(text, TokenType.IDENTIFIER)
            self.addToken(token_type, text)

        c = self.advance()
        assert c is not None
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
            if match('='):
                self.addToken(TokenType.BANG_EQUAL)
            else:
                self.addToken(TokenType.BANG)
        elif c == '=':
            if match('='):
                self.addToken(TokenType.EQUAL_EQUAL)
            else:
                self.addToken(TokenType.EQUAL)
        elif c == '<':
            if match('='):
                self.addToken(TokenType.LESS_EQUAL)
            else:
                self.addToken(TokenType.LESS)
        elif c == '>':
            if match('='):
                self.addToken(TokenType.GREATER_EQUAL)
            else:
                self.addToken(TokenType.GREATER)
        elif c == '/':
            if match('/'):
                # a comment to end of line
                while not self.isAtEnd() and peek() != '\n':
                    self.advance()
            else:
                self.addToken(TokenType.SLASH)
        elif c in [' ', '\r', '\t']:
            pass
        elif c == '\n':
            self._line += 1
        elif c == '"':
            string()
        elif isDigit(c):
            number()
        elif isAlpha(c):
            identifier()
        else:
            raise self._error(f'Unexpected character "{c}"')

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
