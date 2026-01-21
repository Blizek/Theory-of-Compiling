class Node(object):
    def __init__(self):
        self.symbol = ">  "


class MultipleStmts(Node):
    def __init__(self, stmts, lineno):
        Node.__init__(self)
        self.stmts = stmts
        self.lineno = lineno


class ControlStmt(Node):
    def __init__(self, control_stmt, lineno):
        Node.__init__(self)
        self.control_stmt = control_stmt
        self.lineno = lineno


class StatementsSet(Node):
    def __init__(self, stmts, lineno):
        Node.__init__(self)
        self.stmts = stmts
        self.lineno = lineno


class SpecificStmt(Node):
    def __init__(self, specific_stmt, lineno):
        Node.__init__(self)
        self.specific_stmt = specific_stmt
        self.lineno = lineno


class ReturnExpression(Node):
    def __init__(self, expression, lineno):
        Node.__init__(self)
        self.expression = expression
        self.lineno = lineno


class IfElseStmt(Node):
    def __init__(self, rel_expr, if_stmt, else_stmt, lineno):
        Node.__init__(self)
        self.rel_expr = rel_expr
        self.if_stmt = if_stmt
        self.else_stmt = else_stmt
        self.lineno = lineno


class IfStmt(Node):
    def __init__(self, rel_expr, if_stmt, lineno):
        Node.__init__(self)
        self.rel_expr = rel_expr
        self.if_stmt = if_stmt
        self.lineno = lineno


class WhileStmt(Node):
    def __init__(self, rel_expr, while_stmt, lineno):
        Node.__init__(self)
        self.rel_expr = rel_expr
        self.while_stmt = while_stmt
        self.lineno = lineno


class ForStmt(Node):
    def __init__(self, iter_variable, range_begin, range_end, for_stmt, lineno):
        Node.__init__(self)
        self.iter_variable = iter_variable
        self.range_begin = range_begin
        self.range_end = range_end
        self.for_stmt = for_stmt
        self.lineno = lineno


class PrintStmt(Node):
    def __init__(self, print_stmt, lineno):
        Node.__init__(self)
        self.print_stmt = print_stmt
        self.lineno = lineno


class PrintRecursive(Node):
    def __init__(self, print_rec, print_expr, lineno):
        Node.__init__(self)
        self.print_rec = print_rec
        self.print_expr = print_expr
        self.lineno = lineno


class PrintExpr(Node):
    def __init__(self, print_expr, lineno):
        Node.__init__(self)
        self.print_expr = print_expr
        self.lineno = lineno


class Value(Node):
    def __init__(self, val, lineno):
        Node.__init__(self)
        self.val = val
        self.lineno = lineno


class ArithNumExpr(Node):
    def __init__(self, op, left, right, lineno):
        Node.__init__(self)
        self.op = op
        self.left = left
        self.right = right
        self.lineno = lineno
        

class Variable(Node):
    def __init__(self, name, lineno):
        Node.__init__(self)
        self.name = name
        self.lineno = lineno


class IntNum(Node):
    def __init__(self, value, lineno):
        Node.__init__(self)
        self.value = value
        self.lineno = lineno


class AssignExpression(Node):
    def __init__(self, expression, lineno):
        Node.__init__(self)
        self.expression = expression
        self.lineno = lineno


class RelationExpression(Node):
    def __init__(self, expression, lineno):
        Node.__init__(self)
        self.expression = expression
        self.lineno = lineno


class MatrixExpression(Node):
    def __init__(self, expression, lineno):
        Node.__init__(self)
        self.expression = expression
        self.lineno = lineno


class UnaryExpression(Node):
    def __init__(self, op, expression, lineno):
        Node.__init__(self)
        self.op = op
        self.expression = expression
        self.lineno = lineno


class MatrixNode(Node):
    def __init__(self, values, lineno):
        Node.__init__(self)
        self.values = values
        self.lineno = lineno


class GeneralExpression(Node):
    def __init__(self, expression, special_op, lineno):
        Node.__init__(self)
        self.expression = expression
        self.special_op = special_op
        self.lineno = lineno


class ArithMatExpr(Node):
    def __init__(self, op, left, right, lineno):
        Node.__init__(self)
        self.div_op = op
        self.left = left
        self.right = right
        self.lineno = lineno


class DeclareExpr(Node):
    def __init__(self, op, left, right, lineno):
        Node.__init__(self)
        self.op = op
        self.left = left
        self.right = right
        self.lineno = lineno


class UpdateExpr(Node):
    def __init__(self, op, left, right, lineno):
        Node.__init__(self)
        self.assign_op = op
        self.left = left
        self.right = right
        self.lineno = lineno

        
class CompExpr(Node):
    def __init__(self, op, left, right, lineno):
        Node.__init__(self)
        self.comp_op = op
        self.left = left
        self.right = right
        self.lineno = lineno


class MatrixRef(Node):
    def __init__(self, matrix_ref, lineno):
        Node.__init__(self)
        self.matrix_ref = matrix_ref
        self.lineno = lineno


class TabRef(Node):
    def __init__(self, tab_ref, lineno):
        Node.__init__(self)
        self.tab_ref = tab_ref
        self.lineno = lineno


class DoubleRef(Node):
    def __init__(self, id, row, col, lineno):
        Node.__init__(self)
        self.id = id
        self.row = row
        self.col = col
        self.lineno = lineno


class SingleRef(Node):
    def __init__(self, id, row, lineno):
        Node.__init__(self)
        self.id = id
        self.row = row
        self.lineno = lineno


class TabRefBoth(Node):
    def __init__(self, id, begin, end, lineno):
        Node.__init__(self)
        self.id = id
        self.begin = begin
        self.end = end
        self.lineno = lineno


class TabRefEnd(Node):
    def __init__(self, id, end, lineno):
        Node.__init__(self)
        self.id = id
        self.end = end
        self.lineno = lineno


class TabRefBegin(Node):
    def __init__(self, id, begin, lineno):
        Node.__init__(self)
        self.id = id
        self.begin = begin
        self.lineno = lineno


class MatrixRowsNode(Node):
    def __init__(self, rows, lineno):
        Node.__init__(self)
        self.rows = rows
        self.lineno = lineno


class NumLineNode(Node):
    def __init__(self, num_line, lineno):
        Node.__init__(self)
        self.num_line = num_line
        self.lineno = lineno


class MatrixFuncs(Node):
    def __init__(self, fun, value, lineno):
        Node.__init__(self)
        self.fun = fun
        self.value = value
        self.lineno = lineno


class FloatNum(Node):
    def __init__(self, value, lineno):
        Node.__init__(self)
        self.value = value
        self.lineno = lineno


class String(Node):
    def __init__(self, value, lineno):
        Node.__init__(self)
        self.value = value
        self.lineno = lineno


class Error(Node):
    def __init__(self):
        pass