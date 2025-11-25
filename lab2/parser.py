from sly import Parser
from scanner import Scanner

class Mparser(Parser):
    tokens = Scanner.tokens
    debugfile = 'parser.out'

    precedence = (
        ("nonassoc", IFX),
        ("nonassoc", ELSE),
        ("nonassoc", LE, GE, EQ, NE, "<", ">"),
        ("left", '+', '-'),
        ("left", '*', '/'),
        ("left", DOTADD, DOTSUB),
        ("left", DOTMUL, DOTDIV),
        ("right", UMINUS)
    )

    @_('statements statement',
       'statement')
    def statements(self, p):
        pass

    @_('";"',
       '"{" statements "}"',
       'if_statement',
       'while_statement',
       'for_statement',
       'assign_expression',
       'print_statement',
       'BREAK ";"',
       'CONTINUE ";"',
       'RETURN expression ";"')
    def statement(self, p):
        pass

    @_('IF "(" relation_expression ")" statement ELSE statement',
       'IF "(" relation_expression ")" statement %prec IFX')
    def if_statement(self, p):
        pass

    @_('WHILE "(" relation_expression ")" statement')
    def while_statement(self, p):
        pass

    @_('FOR ID "=" id_int ":" id_int statement')
    def for_statement(self, p):
        pass

    @_('PRINT print_recursive ";"')
    def print_statement(self, p):
        pass

    @_('print_recursive "," value',
       'value')
    def print_recursive(self, p):
        pass

    @_('ID',
       'INTNUM')
    def id_int(self, p):
        pass

    @_('value',
       'assign_expression',
       'relation_expression',
       'matrix_funcs',
       'matrix_ref',
       '"-" expression %prec UMINUS',
       '"[" matrix_rows "]"',
       '"[" line_of_num "]"',
       'expression "\'"')
    def expression(self, p):
        pass

    @_('expression "+" expression',
       'expression "-" expression',
       'expression "*" expression',
       'expression "/" expression')
    def expression(self, p):
        pass

    @_('expression DOTADD expression',
       'expression DOTSUB expression',
       'expression DOTMUL expression',
       'expression DOTDIV expression')
    def expression(self, p):
        pass

    @_('id_ref "=" expression ";"',
       'id_ref ADDASSIGN expression ";"',
       'id_ref SUBASSIGN expression ";"',
       'id_ref MULASSIGN expression ";"',
       'id_ref DIVASSIGN expression ";"', )
    def assign_expression(self, p):
        pass

    @_('expression "<" expression',
       'expression ">" expression',
       'expression LE expression',
       'expression GE expression',
       'expression EQ expression',
       'expression NE expression', )
    def relation_expression(self, p):
        pass

    @_('ID',
       'matrix_ref',
       'tab_ref')
    def id_ref(self, p):
        pass

    @_('ID "[" id_int "," id_int "]"',
       'ID "[" id_int "]"')
    def matrix_ref(self, p):
        pass

    @_('ID "[" id_int : id_int "]"',
       'ID "["  : id_int "]"',
       'ID "[" id_int :  "]"')
    def tab_ref(self, p):
        pass

    @_('matrix_rows "," "[" line_of_num "]"',
       '"[" line_of_num "]"')
    def matrix_rows(self, p):
        pass

    @_('INTNUM',
       'line_of_num "," INTNUM')
    def line_of_num(self, p):
        pass

    @_('ZEROS "(" INTNUM ")"',
       'ONES "(" INTNUM ")"',
       'EYE "(" INTNUM ")"')
    def matrix_funcs(self, p):
        pass

    @_('INTNUM',
       'FLOATNUM',
       'ID',
       'STRING')
    def value(self, p):
        pass