from tok import Token, TokenType

from typing import List


class Scanner:
    def __init__(self, text: str):
        self._text = text
        self._tokens: List[Token] = []
        self._start = 0
        self._current = 0
        self._line = 1

    def tokens(self) -> List[str]:
        self._tokens.append(Token(TokenType.EOF, '', None, self._line))
        return self._tokens
