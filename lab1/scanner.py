import sys
import re
from sly import Lexer


class Scanner(Lexer):
    tokens = {DOTADD, DOTSUB, DOTMUL, DOTDIV, TRANSPOSE,
              ADDASSIGN, SUBASSIGN, MULASSIGN, DIVASSIGN,
              LT, GT, LE, GE, EQ, NE,
              IF, ELSE, FOR, WHILE, BREAK, CONTINUE, RETURN,
              EYE, ZEROS, ONES, PRINT,
              ID, INTNUM, FLOATNUM, STRING}

    literals = {'(', ')', '{', '}', '[', ']', '+', '-', '*', '/', ':', ',', ';', '=', '\''}

    # Regular expression rules for tokens
    DOTADD = r'\.\+'
    DOTSUB = r'\.-'
    DOTMUL = r'\.\*'
    DOTDIV = r'\./'

    ADDASSIGN = r'\+='
    SUBASSIGN = r'-='
    MULASSIGN = r'\*='
    DIVASSIGN = r'/='

    LT = r'<'
    GT = r'>'
    LE = r'<='
    GE = r'>='
    EQ = r'=='
    NE = r'!='

    # Identifiers and keywords
    ID = r'[a-zA-Z_][a-zA-Z0-9_]*'
    ID['if'] = IF
    ID['else'] = ELSE
    ID['for'] = FOR
    ID['while'] = WHILE
    ID['break'] = BREAK
    ID['continue'] = CONTINUE
    ID['return'] = RETURN
    ID['eye'] = EYE
    ID['zeros'] = ZEROS
    ID['ones'] = ONES
    ID['print'] = PRINT

    @_(r'"([^"\\]|\\.)*"')
    def STRING(self, t):
        self.update_lineno(t.value)
        return t

    @_(r'((\d+\.\d*|\.\d+)([eE][-+]?\d+)?|\d+[eE][-+]?\d+)')
    def FLOATNUM(self, t):
        t.value = float(t.value)
        return t

    @_(r'\d+')
    def INTNUM(self, t):
        t.value = int(t.value)
        return t

    # String containing ignored characters
    ignore = ' \t'
    ignore_comment = r'\#.*'

    # Line number tracking
    @_(r'\n+')
    def ignore_newline(self, t):
        self.lineno += t.value.count('\n')

    def update_lineno(self, string):
        self.lineno += string.count('\n')

    def error(self, t):
        print('Line %d: Bad character %r' % (self.lineno, t.value[0] if t.value else ''))
        self.index += 1


if __name__ == '__main__':

    lexer = Scanner()

    filename = sys.argv[1] if len(sys.argv) > 1 else "example.txt"
    with open(filename, "r") as file:
        text = file.read()

    for tok in lexer.tokenize(text):
        print(f"{tok.lineno}: {tok.type}({tok.value})")