from lexeme import Lexeme, TokenType

class LexAnalyze:
    def __init__(self):
        self.tokens = []
        self.keywords = {"int", "for", "if", "else", "return"}

    def lex(self, code: str):
        self.tokens.clear()
        
        # Normalize newlines to '\n'
        code = code.replace("\r\n", "\n").replace("\r", "\n")

        i = 0
        line = 1
        col = 1

        def peek(offset=0):
            idx = i + offset
            return code[idx] if idx < len(code) else "\0"

        while i < len(code):
            c = peek()

            # Skip whitespace (now only '\n' exists for newlines)
            if c.isspace():
                if c == "\n":
                    line += 1
                    col = 1
                else:
                    col += 1
                i += 1
                continue

            # Comments (// or /* */)
            if c == "/":
                n = peek(1)

                # Line comment
                if n == "/":
                    i += 2
                    col += 2
                    while i < len(code) and peek() != "\n":
                        i += 1
                        col += 1
                    continue

                # Block comment
                if n == "*":
                    i += 2
                    col += 2
                    while i < len(code):
                        if peek() == "\n":
                            line += 1
                            col = 1
                            i += 1
                        elif peek() == "*" and peek(1) == "/":
                            i += 2
                            col += 2
                            break
                        else:
                            i += 1
                            col += 1
                    continue

            # Identifier / Keyword
            if c.isalpha() or c == "_":
                start_line = line
                start_col = col
                s = ""

                while peek().isalnum() or peek() == "_":
                    s += peek()
                    i += 1
                    col += 1

                token_type = TokenType.KEYWORD if s in self.keywords else TokenType.ID
                self.tokens.append(Lexeme(token_type, s, start_line, start_col))
                continue

            # Number
            if c.isdigit():
                start_line = line
                start_col = col
                s = ""

                while peek().isdigit():
                    s += peek()
                    i += 1
                    col += 1

                self.tokens.append(Lexeme(TokenType.NUMBER, s, start_line, start_col))
                continue

            # String literal
            if c == '"':
                start_line = line
                start_col = col

                s = '"'
                i += 1
                col += 1

                while i < len(code):
                    ch = peek()
                    s += ch
                    i += 1

                    if ch == "\n":
                        line += 1
                        col = 1
                    else:
                        col += 1

                    if ch == '"':
                        break

                self.tokens.append(Lexeme(TokenType.STRING, s, start_line, start_col))
                continue

            # Char literal
            if c == "'":
                start_line = line
                start_col = col

                s = "'"
                i += 1
                col += 1

                while i < len(code):
                    ch = peek()
                    s += ch
                    i += 1

                    if ch == "\n":
                        line += 1
                        col = 1
                    else:
                        col += 1

                    if ch == "'":
                        break

                self.tokens.append(Lexeme(TokenType.CHAR, s, start_line, start_col))
                continue

            # Multi-character operators (maximal munch)
            start_line = line
            start_col = col

            if c == "!" and peek(1) == "=":
                self.tokens.append(Lexeme(TokenType.NOTEQUAL, "!=", start_line, start_col))
                i += 2
                col += 2
                continue

            if c == "+" and peek(1) == "=":
                self.tokens.append(Lexeme(TokenType.PLUSEQUAL, "+=", start_line, start_col))
                i += 2
                col += 2
                continue

            if c == "-" and peek(1) == "=":
                self.tokens.append(Lexeme(TokenType.MINUSEQUAL, "-=", start_line, start_col))
                i += 2
                col += 2
                continue

            # Single-character tokens
            single_char_tokens = {
                "(": TokenType.LPAREN,
                ")": TokenType.RPAREN,
                "{": TokenType.LBRACE,
                "}": TokenType.RBRACE,
                ",": TokenType.COMMA,
                ";": TokenType.SEMICOLON,
                "=": TokenType.EQUALS,
                ">": TokenType.GREATER,
            }

            if c in single_char_tokens:
                self.tokens.append(Lexeme(single_char_tokens[c], c, start_line, start_col))
                i += 1
                col += 1
                continue

            # Unknown character
            self.tokens.append(Lexeme(TokenType.UNKNOWN, c, start_line, start_col))
            i += 1
            col += 1