from LexAnalyze import LexAnalyze

source_code = """int calculate() {\n
 int count = 0, value = 10;\n
 for (; value > count;) {\n
 count += 2; /* Increment count by 2 */\n
 }\n
 return count;\n
}\n"""

lexer = LexAnalyze()
lexer.lex(source_code)

W_SN, W_LEX, W_TOKEN, W_LINE = 8, 18, 18, 10

def pad(s, w):
    s = str(s)
    return s + " " * max(0, w - len(s))

# Header
header = (
    pad("S. No.", W_SN) +
    pad("Lexeme", W_LEX) +
    pad("Token", W_TOKEN) +
    pad("Line No.", W_LINE)
)
print(header)
print("-" * (W_SN + W_LEX + W_TOKEN + W_LINE))

row_num = 1
for tok in lexer.tokens:

    sn = f"{row_num}."
    lex = tok.val
    token_name = tok.type_to_string() 
    line = tok.line

    print(
        pad(sn, W_SN) +
        pad(lex, W_LEX) +
        pad(token_name, W_TOKEN) +
        pad(line, W_LINE)
    )
    row_num += 1
