class Node(object):
    pass


class MultipleStmts(Node):
    def __init__(self, stmts, lineno):
        self.stmts = stmts
        self.lineno = lineno


class ControlStmt(Node):
    def __init__(self, control_stmt, lineno):
        self.control_stmt = control_stmt
        self.lineno = lineno


class StatementsSet(Node):
    def __init__(self, stmts, lineno):
        self.stmts = stmts
        self.lineno = lineno


class SpecificStmt(Node):
    def __init__(self, specific_stmt, lineno):
        self.specific_stmt = specific_stmt
        self.lineno = lineno


class ReturnExpression(Node):
    def __init__(self, expression, lineno):
        self.expression = expression
        self.lineno = lineno


class IfElseStmt(Node):
    def __init__(self, rel_expr, if_stmt, else_stmt, lineno):
        self.rel_expr = rel_expr
        self.if_stmt = if_stmt
        self.else_stmt = else_stmt
        self.lineno = lineno


class IfStmt(Node):
    def __init__(self, rel_expr, if_stmt, lineno):
        self.rel_expr = rel_expr
        self.if_stmt = if_stmt
        self.lineno = lineno


class WhileStmt(Node):
    def __init__(self, rel_expr, while_stmt, lineno):
        self.rel_expr = rel_expr
        self.while_stmt = while_stmt
        self.lineno = lineno


class ForStmt(Node):
    def __init__(self, iter_variable, range_begin, range_end, for_stmt, lineno):
        self.iter_variable = iter_variable
        self.range_begin = range_begin
        self.range_end = range_end
        self.for_stmt = for_stmt
        self.lineno = lineno


class PrintStmt(Node):
    def __init__(self, print_stmt, lineno):
        self.print_stmt = print_stmt
        self.lineno = lineno


class PrintRecursive(Node):
    def __init__(self, print_rec, val, lineno):
        self.print_rec = print_rec
        self.val = val
        self.lineno = lineno


class Value(Node):
    def __init__(self, val, lineno):
        self.val = val
        self.lineno = lineno


class Variable(Node):
    def __init__(self, name, lineno):
        self.name = name
        self.lineno = lineno


class IntNum(Node):
    def __init__(self, value, lineno):
        self.value = value
        self.lineno = lineno


class AssignExpression(Node):
    def __init__(self, expression, lineno):
        self.expression = expression
        self.lineno = lineno


class DeclareExpr(Node):
    def __init__(self, op, left, right, lineno):
        self.op = op
        self.left = left
        self.right = right
        self.lineno = lineno


class RelationExpression(Node):
    def __init__(self, expression, lineno):
        self.expression = expression
        self.lineno = lineno


class MatrixExpression(Node):
    def __init__(self, expression, lineno):
        self.expression = expression
        self.lineno = lineno


class UnaryExpression(Node):
    def __init__(self, op, expression, lineno):
        self.op = op
        self.expression = expression
        self.lineno = lineno


class MatrixRowsNode(Node):
    def __init__(self, rows, lineno):
        self.rows = rows
        self.lineno = lineno


class NumLineNode(Node):
    def __init__(self, num_line, lineno):
        self.num_line = num_line
        self.lineno = lineno


class GeneralExpression(Node):
    def __init__(self, expression, lineno):
        self.expression = expression
        self.lineno = lineno


class BinExpr(Node):
    def __init__(self, op, left, right, lineno):
        self.op = op
        self.left = left
        self.right = right
        self.lineno = lineno


class MatrixRef(Node):
    def __init__(self, matrix_ref, lineno):
        self.matrix_ref = matrix_ref
        self.lineno = lineno


class TabRef(Node):
    def __init__(self, tab_ref, lineno):
        self.tab_ref = tab_ref
        self.lineno = lineno


class IndexRef(Node):
    def __init__(self, id, index_list, lineno):
        self.id = id
        self.index_list = index_list
        self.lineno = lineno


class TabRefBoth(Node):
    def __init__(self, id, begin, end, lineno):
        self.id = id
        self.begin = begin
        self.end = end
        self.lineno = lineno


class TabRefEnd(Node):
    def __init__(self, id, end, lineno):
        self.id = id
        self.end = end
        self.lineno = lineno


class TabRefBegin(Node):
    def __init__(self, id, begin, lineno):
        self.id = id
        self.begin = begin
        self.lineno = lineno


class MatrixFuncs(Node):
    def __init__(self, fun, value, lineno):
        self.fun = fun
        self.value = value
        self.lineno = lineno


class FloatNum(Node):
    def __init__(self, value, lineno):
        self.value = value
        self.lineno = lineno


class String(Node):
    def __init__(self, value, lineno):
        self.value = value
        self.lineno = lineno


class Error(Node):
    def __init__(self):
        pass


class MatrixNode(Node):
    def __init__(self, values, lineno):
        self.values = values
        self.lineno = lineno