from typing import Optional, Sequence

from expression import Binary, Expression, Grouping, Literal, Unary
from tok import Token, TokenType


class ParseError(Exception):
    pass


class Parser:
    def __init__(self, tokens: Sequence[Token]):
        self._tokens = tokens
        self._current = 0

    def parse(self) -> Expression:
        return self._expression()

    #      _        _                         _
    #  ___| |_ __ _| |_ ___    __ _ _ __   __| |
    # / __| __/ _` | __/ _ \  / _` | '_ \ / _` |
    # \__ \ || (_| | ||  __/ | (_| | | | | (_| |
    # |___/\__\__,_|\__\___|  \__,_|_| |_|\__,_|
    #                  _        _   _
    #  _ __ ___  _   _| |_ __ _| |_(_) ___  _ __
    # | '_ ` _ \| | | | __/ _` | __| |/ _ \| '_ \
    # | | | | | | |_| | || (_| | |_| | (_) | | | |
    # |_| |_| |_|\__,_|\__\__,_|\__|_|\___/|_| |_|
    #  FIGLET: state and mutation
    #

    def _isAtEnd(self) -> bool:
        return self._peek().token_type == TokenType.EOF

    def _advance(self) -> Optional[Token]:
        if self._isAtEnd():
            return None
        self._current += 1
        return self._previous()

    def _peek(self) -> Token:
        if self._current == 0 and len(self._tokens) == 0:
            raise ParseError('No tokens to parse')
        return self._tokens[self._current]

    def _previous(self) -> Token:
        if self._current == 0:
            raise ParseError('Cannot fetch previous to first token')
        return self._tokens[self._current - 1]

    #                             _                     _ _ _
    #   ___ _ __ _ __ ___  _ __  | |__   __ _ _ __   __| | (_)_ __   __ _
    #  / _ \ '__| '__/ _ \| '__| | '_ \ / _` | '_ \ / _` | | | '_ \ / _` |
    # |  __/ |  | | | (_) | |    | | | | (_| | | | | (_| | | | | | | (_| |
    #  \___|_|  |_|  \___/|_|    |_| |_|\__,_|_| |_|\__,_|_|_|_| |_|\__, |
    #                                                               |___/
    #  FIGLET: error handling
    #
    def _error(self, token: Token, message: str) -> ParseError:
        # TODO use an error reporter implementation
        m = f'{token} {message}'
        return ParseError(m)

    #                       _               _          _
    #  _ __   __ _ _ __ ___(_)_ __   __ _  | |__   ___| |_ __   ___ _ __ ___
    # | '_ \ / _` | '__/ __| | '_ \ / _` | | '_ \ / _ \ | '_ \ / _ \ '__/ __|
    # | |_) | (_| | |  \__ \ | | | | (_| | | | | |  __/ | |_) |  __/ |  \__ \
    # | .__/ \__,_|_|  |___/_|_| |_|\__, | |_| |_|\___|_| .__/ \___|_|  |___/
    # |_|                           |___/               |_|
    #  FIGLET: parsing helpers
    #

    def _check(self, token_type: TokenType) -> bool:
        if self._isAtEnd():
            return False
        return self._peek().token_type == token_type

    def _match(self, token_types: Sequence[TokenType]) -> bool:
        for token_type in token_types:
            if self._check(token_type):
                self._advance()
                return True
        return False

    def _consume(self, token_type: TokenType, message: str) -> Token:
        if self._check(token_type):
            return self._advance()
        raise self._error(self._peek(), message)

    def _synchronize(self) -> None:
        self._advance()
        while not self._isAtEnd():
            if self._previous().type == TokenType.SEMICOLON:
                return
            if self._peek().type in [
                TokenType.CLASS,
                TokenType.FOR,
                TokenType.FUN,
                TokenType.IF,
                TokenType.PRINT,
                TokenType.RETURN,
                TokenType.VAR,
                TokenType.WHILE,
            ]:
                return
            self._advance()

    #                       _                          _
    #  _ __   __ _ _ __ ___(_)_ __   __ _   _ __ _   _| | ___  ___
    # | '_ \ / _` | '__/ __| | '_ \ / _` | | '__| | | | |/ _ \/ __|
    # | |_) | (_| | |  \__ \ | | | | (_| | | |  | |_| | |  __/\__ \
    # | .__/ \__,_|_|  |___/_|_| |_|\__, | |_|   \__,_|_|\___||___/
    # |_|                           |___/
    #  FIGLET: parsing rules
    #

    def _expression(self) -> Expression:
        return self._equality()

    def _equality(self) -> Expression:
        expression = self._comparison()

        while self._match([TokenType.BANG_EQUAL, TokenType.EQUAL_EQUAL]):
            operator = self._previous()
            right = self._comparison()
            expression = Binary(left=expression, operator=operator, right=right)
        return expression

    def _comparison(self) -> Expression:
        expression = self._additive()

        while self._match(
            [
                TokenType.LESS,
                TokenType.LESS_EQUAL,
                TokenType.GREATER,
                TokenType.GREATER_EQUAL,
            ]
        ):
            operator = self._previous()
            right = self._additive()
            expression = Binary(left=expression, operator=operator, right=right)
        return expression

    def _additive(self) -> Expression:
        expression = self._multiplicative()

        while self._match([TokenType.PLUS, TokenType.MINUS]):
            operator = self._previous()
            right = self._multiplicative()
            expression = Binary(left=expression, operator=operator, right=right)
        return expression

    def _multiplicative(self) -> Expression:
        expression = self._unary()

        while self._match([TokenType.SLASH, TokenType.STAR]):
            operator = self._previous()
            right = self._unary()
            expression = Binary(left=expression, operator=operator, right=right)
        return expression

    def _unary(self) -> Expression:
        if self._match([TokenType.BANG, TokenType.MINUS]):
            operator = self._previous()
            expression = self._unary()
            return Unary(operator=operator, expression=expression)
        return self._primary()

    def _primary(self) -> Expression:
        if self._match([TokenType.FALSE]):
            return Literal(value=False)
        elif self._match([TokenType.TRUE]):
            return Literal(value=True)
        elif self._match([TokenType.NIL]):
            return Literal(value=None)
        elif self._match([TokenType.NUMBER, TokenType.STRING]):
            return Literal(value=self._previous().literal)
        elif self._match([TokenType.LEFT_PAREN]):
            expression = self._expression()
            self._consume(TokenType.RIGHT_PAREN, "Expected ')' after '('.")
            return Grouping(expression=expression)

        raise self._error(self._peek(), 'Expected expression')

    #  _____                              _
    # | ____|_  ___ __  _ __ ___  ___ ___(_) ___  _ __
    # |  _| \ \/ / '_ \| '__/ _ \/ __/ __| |/ _ \| '_ \
    # | |___ >  <| |_) | | |  __/\__ \__ \ | (_) | | | |
    # |_____/_/\_\ .__/|_|  \___||___/___/_|\___/|_| |_|
    #            |_|
    # __     ___     _ _
    # \ \   / (_)___(_) |_ ___  _ __
    #  \ \ / /| / __| | __/ _ \| '__|
    #   \ V / | \__ \ | || (_) | |
    #    \_/  |_|___/_|\__\___/|_|
    #  FIGLET: Expression Visitor
    #

    def visit_unary(self, unary: Unary):
        pass

    def visit_binary(self, binary: Binary):
        pass

    def visit_grouping(self, grouping: Grouping):
        pass

    def visit_literal(self, literal: Literal):
        pass
