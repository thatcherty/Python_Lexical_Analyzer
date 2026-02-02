from lexeme import Lexeme, TokenType

class LexAnalyze:
    def __init__(self):
        self.tokens = []
        self.keywords = {"int", "for", "if", "else", "return"}

    def lex(self, code: str):
        self.tokens.clear()

        i = 0
        line = 1
        col = 1

        def peek(offset=0):
            if i + offset >= len(code):
                return '\0'
            return code[i + offset]

        while i < len(code):
            c = peek()

            # --- Skip whitespace ---
            if c.isspace():
                if c == '\n':
                    line += 1
                    col = 1
                else:
                    col += 1
                i += 1
                continue

            # --- Comments or divide ---
            if c == '/':
                n = peek(1)
                if n == '/':           # line comment
                    i += 2
                    col += 2
                    while i < len(code) and peek() != '\n':
                        i += 1
                        col += 1
                    continue
                if n == '*':           # block comment
                    i += 2
                    col += 2
                    while i < len(code):
                        if peek() == '\n':
                            line += 1
                            col = 1
                            i += 1
                        elif peek() == '*' and peek(1) == '/':
                            i += 2
                            col += 2
                            break
                        else:
                            i += 1
                            col += 1
                    continue

            # --- Identifier / Keyword ---
            if c.isalpha() or c == '_':
                start_col = col
                s = ""
                while peek().isalnum() or peek() == '_':
                    s += peek()
                    i += 1
                    col += 1

                token_type = TokenType.KEYWORD if s in self.keywords else TokenType.ID
                self.tokens.append(Lexeme(token_type, s, line, start_col))
                continue

            # --- Number ---
            if c.isdigit():
                start_col = col
                s = ""
                while peek().isdigit():
                    s += peek()
                    i += 1
                    col += 1

                self.tokens.append(Lexeme(TokenType.NUMBER, s, line, start_col))
                continue

            # --- String literal ---
            if c == '"':
                start_col = col
                s = '"'
                i += 1
                col += 1

                while i < len(code):
                    ch = peek()
                    s += ch
                    i += 1
                    col += 1
                    if ch == '"':
                        break
                    if ch == '\n':
                        line += 1
                        col = 1

                self.tokens.append(Lexeme(TokenType.STRING, s, line, start_col))
                continue

            # --- Char literal ---
            if c == '\'':
                start_col = col
                s = '\''
                i += 1
                col += 1

                while i < len(code):
                    ch = peek()
                    s += ch
                    i += 1
                    col += 1
                    if ch == '\'':
                        break

                self.tokens.append(Lexeme(TokenType.CHAR, s, line, start_col))
                continue

            # --- Multi-character operators ---
            start_col = col
            if c == '!' and peek(1) == '=':
                self.tokens.append(Lexeme(TokenType.NOTEQUAL, "!=", line, start_col))
                i += 2
                col += 2
                continue

            if c == '+' and peek(1) == '=':
                self.tokens.append(Lexeme(TokenType.PLUSEQUAL, "+=", line, start_col))
                i += 2
                col += 2
                continue

            if c == '-' and peek(1) == '=':
                self.tokens.append(Lexeme(TokenType.MINUSEQUAL, "-=", line, start_col))
                i += 2
                col += 2
                continue

            # --- Single-character tokens ---
            single_char_tokens = {
                '(': TokenType.LPAREN,
                ')': TokenType.RPAREN,
                '{': TokenType.LBRACE,
                '}': TokenType.RBRACE,
                ',': TokenType.COMMA,
                ';': TokenType.SEMICOLON,
                '=': TokenType.EQUALS,
                '>': TokenType.GREATER,
            }

            if c in single_char_tokens:
                self.tokens.append(Lexeme(single_char_tokens[c], c, line, col))
                i += 1
                col += 1
                continue

            # --- Unknown ---
            self.tokens.append(Lexeme(TokenType.UNKNOWN, c, line, col))
            i += 1
            col += 1
