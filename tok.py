import enum


class TokenType(enum.Enum):
    LEFT_PAREN = enum.auto()
    RIGHT_PAREN = enum.auto()
    LEFT_BRACE = enum.auto()
    RIGHT_BRACE = enum.auto()

    COMMA = enum.auto()
    DOT = enum.auto()
    MINUS = enum.auto()
    PLUS = enum.auto()
    SEMICOLON = enum.auto()
    SLASH = enum.auto()
    STAR = enum.auto()

    BANG = enum.auto()
    BANG_EQUAL = enum.auto()
    EQUAL = enum.auto()
    EQUAL_EQUAL = enum.auto()
    GREATER = enum.auto()
    GREATER_EQUAL = enum.auto()
    LESS = enum.auto()
    LESS_EQUAL = enum.auto()

    IDENTIFIER = enum.auto()
    STRING = enum.auto()
    NUMBER = enum.auto()

    AND = enum.auto()
    CLASS = enum.auto()
    ELSE = enum.auto()
    FALSE = enum.auto()
    FOR = enum.auto()
    FUN = enum.auto()
    IF = enum.auto()
    NIL = enum.auto()
    OR = enum.auto()
    PRINT = enum.auto()
    RETURN = enum.auto()
    SUPER = enum.auto()
    THIS = enum.auto()
    TRUE = enum.auto()
    VAR = enum.auto()
    WHILE = enum.auto()

    EOF = enum.auto()


class Token:
    def __init__(self, token_type: TokenType, lexeme: str, literal: object, line: int):
        self.token_type = token_type
        self.lexeme = lexeme
        self.literal = literal
        self.line = line

    def __eq__(self, other) -> bool:
        if not isinstance(other, Token):
            return False
        return (
            self.__class__ == other.__class__
            and self.token_type == other.token_type
            and self.lexeme == other.lexeme
            and self.literal == other.literal
            and self.line == other.line
        )

    def __str__(self) -> str:
        return f'{self.__class__.__name__}(type={self.token_type}, lexeme="{self.lexeme}", literal={self.literal}, line={self.line})'
