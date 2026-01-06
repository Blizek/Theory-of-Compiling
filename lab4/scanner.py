import sys
from sly import Lexer

class Scanner(Lexer):
    # Set of nonliteral token names
    tokens = {
                DOTADD, DOTSUB, DOTMUL, DOTDIV,
                ADDASSIGN, SUBASSIGN, MULASSIGN, DIVASSIGN,
                LE, GE, NE, EQ, 
                IF, ELSE, FOR, WHILE, BREAK, CONTINUE, RETURN,
                EYE, ZEROS, ONES, 
                PRINT, ID, INTNUM, FLOATNUM, STRING
             }

    literals = {'+', '-', '*', '/', '=', '<', '>', '(', ')', '[', ']', '{', '}', ':', '\'', ',', ';'}

    # Strings containing ignored characters and comments
    ignore = ' \t'
    ignore_comment = r'\#.*'

    # Regular expression rules for tokens
    DOTADD = r'\.\+'
    DOTSUB = r'\.-'
    DOTMUL = r'\.\*'
    DOTDIV = r'\./'
    ADDASSIGN = r'\+='
    SUBASSIGN = r'-='
    MULASSIGN = r'\*='
    DIVASSIGN = r'/='
    LE = r'<='
    GE = r'>='
    NE = r'!='
    EQ = r'=='

    @_(r'(\d+\.\d*|\.\d+)((E|e)[+-]?\d+)?|\d+(E|e)[+-]?\d+')
    def FLOATNUM(self, t):
        return t

    @_(r'\d+')
    def INTNUM(self, t):
        t.value = int(t.value)
        return t

    @_(r'(".*?")|(\'.*?\')')
    def STRING(self, t):
        t.value = str(t.value)
        return t

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

    # Line number tracking
    @_(r'\n+')
    def ignore_newline(self, t):
        self.lineno += t.value.count('\n')

    # Reporting errors
    def error(self, t):
        print('Wrong input! Line %d: Bad character %r' % (self.lineno, t.value[0]))
        self.index += 1

if __name__ == '__main__':
    try:
        filename = sys.argv[1] if len(sys.argv) > 1 else "examples/example.txt"
        file = open(filename, "r")
    except IOError:
        print("Cannot open {0} file".format(filename))
        sys.exit(0)

    text = file.read()
    lexer = Scanner()

    for tok in lexer.tokenize(text):
        print(f'({tok.lineno}): {tok.type}({tok.value})')