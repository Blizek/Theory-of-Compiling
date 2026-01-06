from sly import Parser
from scanner import Scanner
import AST


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
        ("right", UMINUS),
        ('nonassoc', "'")
    )

    @_('statement',
       'statements statement')
    def statements(self, p):
        if len(p) == 1:
            values = [p[0]]
        else:
            values = p[0].stmts.copy()
            values.append(p[1])
        return AST.MultipleStmts(values, p.lineno)

    @_('BREAK ";"')
    @_('CONTINUE ";"')
    def statement(self, p):
        return AST.ControlStmt(p[0], p.lineno)

    @_('";"')
    def statement(self, p):
        return None

    @_('"{" statements "}"')
    def statement(self, p):
        return AST.StatementsSet(p[1], p.lineno)

    @_('if_statement',
       'while_statement',
       'for_statement',
       'assign_expression',
       'print_statement')
    def statement(self, p):
        return AST.SpecificStmt(p[0], p.lineno)

    @_('RETURN expression ";"')
    def statement(self, p):
        return AST.ReturnExpression(p[1], p.lineno)

    @_('IF "(" relation_expression ")" statement ELSE statement')
    def if_statement(self, p):
        return AST.IfElseStmt(p[2], p[4], p[6], p.lineno)

    @_('IF "(" relation_expression ")" statement %prec IFX')
    def if_statement(self, p):
        return AST.IfStmt(p[2], p[4], p.lineno)

    @_('WHILE "(" relation_expression ")" statement')
    def while_statement(self, p):
        return AST.WhileStmt(p[2], p[4], p.lineno)

    @_('FOR ID "=" id_int ":" id_int statement')
    def for_statement(self, p):
        return AST.ForStmt(p[1], p[3], p[5], p[6], p.lineno)

    @_('PRINT print_recursive ";"')
    def print_statement(self, p):
        return AST.PrintStmt(p[1], p.lineno)

    @_('print_recursive "," value')
    def print_recursive(self, p):
        return AST.PrintRecursive(p[0], p[2], p.lineno)

    @_('value')
    def print_recursive(self, p):
        return AST.Value(p[0], p.lineno)

    @_('ID')
    def id_int(self, p):
        return AST.Variable(p[0], p.lineno)

    @_('INTNUM')
    def id_int(self, p):
        return AST.IntNum(p[0], p.lineno)

    @_('value')
    def expression(self, p):
        return AST.Value(p[0], p.lineno)

    @_('assign_expression')
    def expression(self, p):
        return AST.AssignExpression(p[0], p.lineno)

    @_('relation_expression')
    def expression(self, p):
        return AST.RelationExpression(p[0], p.lineno)

    @_('matrix_funcs',
       'matrix_ref')
    def expression(self, p):
        return AST.MatrixExpression(p[0], p.lineno)

    @_('"-" expression %prec UMINUS')
    def expression(self, p):
        return AST.UnaryExpression(p[0], p[1], p.lineno)

    @_('"[" matrix_rows "]"')
    def expression(self, p):
        return AST.MatrixNode(p[1], p.lineno)

    @_('"[" line_of_num "]"')
    def expression(self, p):
        return AST.MatrixNode(p[1], p.lineno)

    @_('expression "\'"')
    def expression(self, p):
        return AST.GeneralExpression(p[0], p.lineno)

    @_('expression "+" expression',
       'expression "-" expression',
       'expression "*" expression',
       'expression "/" expression')
    def expression(self, p):
        return AST.BinExpr(p[1], p[0], p[2], p.lineno)

    @_('expression DOTADD expression',
       'expression DOTSUB expression',
       'expression DOTMUL expression',
       'expression DOTDIV expression')
    def expression(self, p):
        return AST.BinExpr(p[1], p[0], p[2], p.lineno)

    @_('id_ref "=" expression ";"')
    def assign_expression(self, p):
        return AST.DeclareExpr(p[1], p[0], p[2], p.lineno)

    @_('id_ref ADDASSIGN expression ";"',
       'id_ref SUBASSIGN expression ";"',
       'id_ref MULASSIGN expression ";"',
       'id_ref DIVASSIGN expression ";"', )
    def assign_expression(self, p):
        return AST.BinExpr(p[1], p[0], p[2], p.lineno)

    @_('expression "<" expression',
       'expression ">" expression',
       'expression LE expression',
       'expression GE expression',
       'expression EQ expression',
       'expression NE expression', )
    def relation_expression(self, p):
        return AST.BinExpr(p[1], p[0], p[2], p.lineno)

    @_('ID')
    def id_ref(self, p):
        return AST.Variable(p[0], p.lineno)

    @_('matrix_ref')
    def id_ref(self, p):
        return AST.MatrixRef(p[0], p.lineno)

    @_('tab_ref')
    def id_ref(self, p):
        return AST.TabRef(p[0], p.lineno)

    @_('ID "[" id_int "," id_int "]"')
    def matrix_ref(self, p):
        return AST.DoubleRef(p[0], p[2], p[4], p.lineno)

    @_('ID "[" id_int "]"')
    def matrix_ref(self, p):
        return AST.SingleRef(p[0], p[2], p.lineno)

    @_('ID "[" id_int ":" id_int "]"')
    def tab_ref(self, p):
        return AST.TabRefBoth(p[0], p[2], p[4], p.lineno)

    @_('ID "["  ":" id_int "]"')
    def tab_ref(self, p):
        return AST.TabRefEnd(p[0], p[3], p.lineno)

    @_('ID "[" id_int ":"  "]"')
    def tab_ref(self, p):
        return AST.TabRefBegin(p[0], p[2], p.lineno)

    @_('"[" line_of_num "]"',
       'matrix_rows "," "[" line_of_num "]"')
    def matrix_rows(self, p):
        if len(p) == 3:
            return AST.MatrixRowsNode([p[1]], p.lineno)

        rows = p[0].rows.copy()
        rows.append(p[3])

        return AST.MatrixRowsNode(rows, p.lineno)

    @_('INTNUM',
       'line_of_num "," INTNUM')
    def line_of_num(self, p):
        if len(p) == 1:
            values = [p[0]]
        else:
            values = p[0].num_line.copy()
            values.append(p[2])

        return AST.NumLineNode(values, p.lineno)

    @_('ZEROS "(" INTNUM ")"',
       'ONES "(" INTNUM ")"',
       'EYE "(" INTNUM ")"')
    def matrix_funcs(self, p):
        return AST.MatrixFuncs(p[0], p[2], p.lineno)

    @_('INTNUM')
    def value(self, p):
        return AST.IntNum(p[0], p.lineno)

    @_('FLOATNUM')
    def value(self, p):
        return AST.FloatNum(p[0], p.lineno)

    @_('ID')
    def value(self, p):
        return AST.Variable(p[0], p.lineno)

    @_('STRING')
    def value(self, p):
        return AST.String(p[0], p.lineno)