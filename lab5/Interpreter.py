import AST
from Memory import *
from Exceptions import *
from visit import *
import sys

operations = {
    '+': lambda x, y: x + y,
    '-': lambda x, y: x - y,
    '/': lambda x, y: x / y if y != 0 else float('inf'),
    '.+': lambda x, y: x + y,
    '.-': lambda x, y: x - y,
    './': lambda x, y: x / y if y != 0 else float('inf'),
    '*': lambda x, y: x * y,
}
sys.setrecursionlimit(10000)


class Interpreter(object):
    def __init__(self):
        # global memory
        self.memory_stack = MemoryStack(Memory("global_memory"))

    @on('node')
    def visit(self, node):
        pass

    @when(AST.MultipleStmts)
    def visit(self, node):
        for stmt in node.stmts:
            self.visit(stmt)

    @when(AST.ControlStmt)
    def visit(self, node):
        if node.control_stmt == "continue":
            raise ContinueException
        elif node.control_stmt == "break":
            raise BreakException

    @when(AST.StatementsSet)
    def visit(self, node):
        self.memory_stack.push(Memory("stmts_set"))

        try:
            self.visit(node.stmts)
        except ReturnValueException:
            return
        finally:
            self.memory_stack.pop()

    @when(AST.SpecificStmt)
    def visit(self, node):
        self.visit(node.specific_stmt)

    @when(AST.ReturnExpression)
    def visit(self, node):
        self.visit(node.expression)
        raise ReturnValueException

    @when(AST.IfElseStmt)
    def visit(self, node):
        if self.visit(node.rel_expr):
            try:
                self.memory_stack.push(Memory("if_stmt"))
                self.visit(node.if_stmt)
            finally:
                self.memory_stack.pop()
        
        else:
            try:
                self.memory_stack.push(Memory("else_stmt"))
                self.visit(node.else_stmt)
            finally:
                self.memory_stack.pop()

    @when(AST.IfStmt)
    def visit(self, node):
        if self.visit(node.rel_expr):
            try:
                self.memory_stack.push(Memory("if_stmt"))
                self.visit(node.if_stmt)
            finally:
                self.memory_stack.pop()

    # simplistic while loop interpretation
    @when(AST.WhileStmt)
    def visit(self, node):
        self.memory_stack.push(Memory("while_stmt"))

        while self.visit(node.rel_expr):
            try:
                self.visit(node.while_stmt)
            except ContinueException:
                pass
            except BreakException:
                break

        self.memory_stack.pop()

    @when(AST.ForStmt)
    def visit(self, node):
        name = node.iter_variable
        value = self.visit(node.range_begin)
        value_end = self.visit(node.range_end)

        self.memory_stack.push(Memory("for_stmt"))
        self.memory_stack.insert(name, value)

        while value < value_end:
            try:
                value = self.memory_stack.get(name)
                self.visit(node.for_stmt)
            except ContinueException:
                pass
            except BreakException:
                break
            finally:
                self.memory_stack.set(name, value + 1)

        self.memory_stack.pop()

    @when(AST.PrintStmt)
    def visit(self, node):
        print(self.visit(node.print_stmt))

    @when(AST.PrintRecursive)
    def visit(self, node):
        text1 = self.visit(node.print_rec)
        text2 = self.visit(node.print_expr)
        return f"{text1} {text2}"

    @when(AST.PrintExpr)
    def visit(self, node):
        return str(self.visit(node.print_expr))

    @when(AST.Value)
    def visit(self, node):
        return self.visit(node.val)

    @when(AST.ArithNumExpr)
    def visit(self, node):
        left = self.visit(node.left)
        right = self.visit(node.right)
        op = node.op
        func = operations[op]
        return func(left, right)

    @when(AST.Variable)
    def visit(self, node):
        return self.memory_stack.get(node.name)

    @when(AST.IntNum)
    def visit(self, node):
        return node.value

    @when(AST.AssignExpression)
    def visit(self, node):
        self.visit(node.expression)

    @when(AST.RelationExpression)
    def visit(self, node):
        return self.visit(node.expression)

    @when(AST.MatrixExpression)
    def visit(self, node):
        val = self.visit(node.expression)
        if isinstance(node.expression, (AST.DoubleRef, AST.SingleRef)):
            name = node.expression.id
            matrix = self.memory_stack.get(name)
            if isinstance(node.expression, AST.DoubleRef):
                return matrix[val[0]][val[1]]
            else:
                return matrix[val[0]]
        return val

    @when(AST.UnaryExpression)
    def visit(self, node):
        return self.visit(node.expression)

    @when(AST.MatrixNode)
    def visit(self, node):
        return self.visit(node.values)

    @when(AST.GeneralExpression)
    def visit(self, node):
        return self.visit(node.expression)

    @when(AST.ArithMatExpr)
    def visit(self, node):
        left = self.visit(node.left)
        right = self.visit(node.right)
        op = node.div_op
        func = operations[op]
        if not all(isinstance(el, list) for el in left) and all(isinstance(el, list) for el in right):
            left = [[l] * len(right[0]) for l in left]
        elif not all(isinstance(el, list) for el in right) and all(isinstance(el, list) for el in left):
            right = [[r] * len(left[0]) for r in right]
        if op == '.*':
            if not all(isinstance(el, list) for el in left) and not all(isinstance(el, list) for el in right):
                return [l * r for l, r in zip(left, right)]

            result = [[0. for _ in range(len(right[0]))] for _ in range(len(left))]

            for i in range(len(left)):
                for j in range(len(right[0])):
                    suma = 0

                    for k in range(len(left[0])):
                        suma += left[i][k] * right[k][j]

                    result[i][j] = suma

            return result
        else:
            if not all(isinstance(el, list) for el in left) and not all(isinstance(el, list) for el in right):
                return [func(l, r) for l, r in zip(left, right)]

            return [[func(l, r) for l, r in zip(lrow, rrow)] for lrow, rrow in zip(left, right)]

    @when(AST.DeclareExpr)
    def visit(self, node):
        if isinstance(node.left, AST.Variable):
            name = node.left.name
            value = self.visit(node.right)

            if self.memory_stack.get(name) is None:
                self.memory_stack.insert(name, value)
            else:
                self.memory_stack.set(name, value)
        else:
            name, indices = self.visit(node.left)
            matrix = self.memory_stack.get(name)
            value = self.visit(node.right)

            if len(indices) == 3:
                begin = 0 if indices[0] is None else indices[0]
                end = len(matrix) if indices[1] is None else indices[1]

                for i in range(begin, end):
                    matrix[i] = value
            elif len(indices) == 2:
                matrix[indices[0]][indices[1]] = value
            else:
                matrix[indices[0]] = value

            self.memory_stack.set(name, matrix)

    @when(AST.UpdateExpr)
    def visit(self, node):
        name = node.left.name
        value = self.visit(node.right)
        op = node.assign_op
        old_value = self.memory_stack.get(name)

        if op == '+=':
            self.memory_stack.set(name, old_value + value)
        elif op == '-=':
            self.memory_stack.set(name, old_value - value)
        elif op == '*=':
            self.memory_stack.set(name, old_value * value)
        elif op == '/=':
            self.memory_stack.set(name, old_value / value)

    @when(AST.CompExpr)
    def visit(self, node):
        left = self.visit(node.left)
        right = self.visit(node.right)
        op = node.comp_op

        if op == '<':
            return left < right
        elif op == '>':
            return left > right
        elif op == '<=':
            return left <= right
        elif op == '>=':
            return left >= right
        elif op == '==':
            return left == right
        elif op == '!=':
            return left != right

    @when(AST.MatrixRef)
    def visit(self, node):
        name = node.matrix_ref.id
        indices = self.visit(node.matrix_ref)
        return name, indices

    @when(AST.TabRef)
    def visit(self, node):
        name = node.tab_ref.id
        indices = self.visit(node.tab_ref)
        return name, indices

    @when(AST.DoubleRef)
    def visit(self, node):
        row = self.visit(node.row)
        col = self.visit(node.col)
        return [row, col]

    @when(AST.SingleRef)
    def visit(self, node):
        row = self.visit(node.row)
        return [row]

    @when(AST.TabRefBoth)
    def visit(self, node):
        begin = self.visit(node.begin)
        end = self.visit(node.end)
        return [begin, end, None]

    @when(AST.TabRefEnd)
    def visit(self, node):
        end = self.visit(node.end)
        return [None, end, None]

    @when(AST.TabRefBegin)
    def visit(self, node):
        begin = self.visit(node.begin)
        return [begin, None, None]

    @when(AST.MatrixRowsNode)
    def visit(self, node):
        return [self.visit(row) for row in node.rows]

    @when(AST.NumLineNode)
    def visit(self, node):
        return node.num_line

    @when(AST.MatrixFuncs)
    def visit(self, node):
        if node.fun == "zeros":
            return [[0. for _ in range(node.value)] for _ in range(node.value)]
        elif node.fun == "ones":
            return [[1. for _ in range(node.value)] for _ in range(node.value)]
        elif node.fun == "eye":
            return [[0. if i != j else 1. for i in range(node.value)] for j in range(node.value)]

    @when(AST.FloatNum)
    def visit(self, node):
        return node.value

    @when(AST.String)
    def visit(self, node):
        return node.value[1:-1]  # because of `""` at the beginning and end
        # I'm not sure why it is like that, but it works

    @when(AST.Error)
    def visit(self, node):
        pass