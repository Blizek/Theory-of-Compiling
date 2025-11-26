from sly import Parser
from scanner import Scanner


class Mparser(Parser):
    tokens = Scanner.tokens
    debugfile = 'parser.out'

    precedence = (
        ("nonassoc", IFX),
        ("nonassoc", ELSE),
        # ("nonassoc", "=", ADDASSIGN, SUBASSIGN, MULASSIGN, DIVASSIGN),
        ("nonassoc", LT, GT, LE, GE, EQ, NE),
        ("left", "+", "-"),
        ("left", DOTADD, DOTSUB),
        ("left", "*", "/"),
        ("left", DOTMUL, DOTDIV),
        ("right", UMINUS),
        ("left", TRANSPOSE),
    )

    @_('statements statement',
       'statement')
    def statements(self, p):
        pass

    @_('IF "(" relation_expression ")" statement %prec IFX',
       'IF "(" relation_expression ")" statement ELSE statement',
       'WHILE "(" relation_expression ")" statement',
       'FOR ID "=" range statement',
       'PRINT print_recursive ";"',
       'assign_statement',
       '"{" statements "}"',
       'BREAK ";"',
       'CONTINUE ";"',
       'RETURN expression ";"')
    def statement(self, p):
        pass

    @_('expression ":" expression')
    def range(self, p):
        pass

    @_('expression',
       'print_recursive "," expression')
    def print_recursive(self, p):
        pass

    @_('id_ref "=" expression ";"',
       'id_ref ADDASSIGN expression ";"',
       'id_ref SUBASSIGN expression ";"',
       'id_ref MULASSIGN expression ";"',
       'id_ref DIVASSIGN expression ";"')
    def assign_statement(self, p):
        pass

    @_('expression "+" expression',
       'expression "-" expression',
       'expression "*" expression',
       'expression "/" expression',
       'expression DOTADD expression',
       'expression DOTSUB expression',
       'expression DOTMUL expression',
       'expression DOTDIV expression')
    def expression(self, p):
        pass

    @_('expression "\'" %prec TRANSPOSE',)
    def expression(self, p):
        pass

    @_('"-" expression %prec UMINUS')
    def expression(self, p):
        pass

    @_('"(" expression ")"')
    def expression(self, p):
        return p.expression

    @_('ID',
       'INTNUM',
       'FLOATNUM',
       'STRING',
       'matrix_funcs',
       'matrix_ref')
    def expression(self, p):
        pass

    @_('"[" matrix_rows "]"')
    def expression(self, p):
        pass

    @_('matrix_rows "," "[" row_content "]"',
       '"[" row_content "]"')
    def matrix_rows(self, p):
        pass

    @_('expression',
       'row_content "," expression')
    def row_content(self, p):
        pass

    @_('ZEROS "(" INTNUM ")"',
       'ONES "(" INTNUM ")"',
       'EYE "(" INTNUM ")"')
    def matrix_funcs(self, p):
        pass

    @_('ID "[" index_list "]"')
    def matrix_ref(self, p):
        pass

    @_('expression',
       'index_list "," expression')
    def index_list(self, p):
        pass

    @_('expression LE expression',
       'expression LT expression',
       'expression GE expression',
       'expression GT expression',
       'expression EQ expression',
       'expression NE expression')
    def relation_expression(self, p):
        pass

    @_('ID')
    def id_ref(self, p):
        pass

    @_('ID "[" index_list "]"')
    def id_ref(self, p):
        pass

    def error(self, p):
        if p:
            print(f"Syntax error at line {p.lineno}, token={p.type}")
        else:
            print("Syntax error at end of file")