from enum import Enum, auto

class TokenType(Enum):
    KEYWORD     = auto()
    ID          = auto()
    NUMBER      = auto()
    STRING      = auto()
    CHAR        = auto()

    LPAREN      = auto()
    RPAREN      = auto()
    LBRACE      = auto()
    RBRACE      = auto()
    COMMA       = auto()
    SEMICOLON   = auto()

    EQUALS      = auto()
    GREATER     = auto()
    PLUSEQUAL   = auto()
    MINUSEQUAL  = auto()
    NOTEQUAL    = auto()

    UNKNOWN     = auto()


class Lexeme:
    def __init__(self, token_type, value, line=1, col=1):
        self.type = token_type
        self.val = value
        self.line = line
        self.col = col

    def type_to_string(self):
        return self.type.name
