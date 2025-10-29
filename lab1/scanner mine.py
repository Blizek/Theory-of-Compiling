import sys
from sly import Lexer


class Scanner(Lexer):
    tokens = {
        # ID
        ID,
        # Binary operators
        PLUS, MINUS, TIMES, DIVIDE,
        # Matrix's binary operators
        DOTPLUS, DOTMINUS, DOTTIMES, DOTDIVIDE,
        # Assign operators
        ASSIGN, PLUSASSIGN, MINUSASSIGN, TIMESASSIGN, DIVIDEASSIGN,
        # Relational operators
        LT, LE, GT, GE, NE, EQ,
        # Keywords
        WHILE, IF, ELSE, FOR, BREAK, CONTINUE, RETURN, EYE, ZEROS, ONES, PRINT,
        # Integer values
        INTNUM,
        # Float values
        FLOATNUM,
        # Strings
        STRINGS
    }

    literals = {'(', ')', '{', '}', '[', ']', ':', ';', "'", '='}

    # String containing ignored characters
    ignore = ' \t'

    # Regular expression rules for tokens
    PLUS    = r'\+'
    MINUS   = r'-'
    TIMES   = r'\*'
    DIVIDE  = r'/'
    EQ      = r'=='
    LE      = r'<='
    LT      = r'<'
    GE      = r'>='
    GT      = r'>'
    NE      = r'!='
    DOTPLUS = r'\.\+'
    DOTMINUS = r'\.\-'
    DOTTIMES = r'\.\*'
    DOTDIVIDE = r'\.\/'


    @_(r'\d+')
    def INTNUM(self, t):
        t.value = int(t.value)
        return t

    # Identifiers and keywords
    ID = r'[a-zA-Z_][a-zA-Z0-9_]*'
    ID['if'] = IF
    ID['else'] = ELSE
    ID['while'] = WHILE
    ID['print'] = PRINT
    ID['zeros'] = ZEROS
    ID['ones'] = ONES
    ID['eye'] = EYE

    ignore_comment = r'\#.*'

    # Line number tracking
    @_(r'\n+')
    def ignore_newline(self, t):
        self.lineno += t.value.count('\n')


if __name__ == '__main__':

    lexer = Scanner()

    filename = sys.argv[1] if len(sys.argv) > 1 else "example.txt"
    with open(filename, "r") as file:
        text = file.read()

    for tok in lexer.tokenize(text):
        print(f"{tok.lineno}: {tok.type}({tok.value})")
