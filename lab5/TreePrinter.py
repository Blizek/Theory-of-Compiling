from __future__ import print_function
import AST

def addToClass(cls):
    def decorator(func):
        setattr(cls, func.__name__, func)
        return func
    return decorator

class Tree:
    def __init__(self, label, children=None):
        self.label = label
        self.children = children if children is not None else []

    def printTree(self, indent=0):
        s = ""
        if self.label is not None:
             s += "|  " * indent + str(self.label) + "\n"

        for child in self.children:
            child_indent = indent + 1 if self.label is not None else indent
            if isinstance(child, Tree):
                s += child.printTree(child_indent)
            elif hasattr(child, 'toTree'):
                 s += child.toTree().printTree(child_indent)
            else: 
                 s += "|  " * (child_indent) + str(child) + "\n"
        return s

class TreePrinter:
    @addToClass(AST.Node)
    def printTree(self, indent=0):
        return self.toTree().printTree(indent)

    @addToClass(AST.MultipleStmts)
    def toTree(self):
        return Tree(None, [stmt.toTree() for stmt in self.stmts])

    @addToClass(AST.ControlStmt)
    def toTree(self):
        return Tree(self.control_stmt.upper())

    @addToClass(AST.StatementsSet)
    def toTree(self):
        return self.stmts.toTree()

    @addToClass(AST.SpecificStmt)
    def toTree(self):
        return self.specific_stmt.toTree()

    @addToClass(AST.ReturnExpression)
    def toTree(self):
        return Tree("RETURN", [self.expression.toTree()])

    @addToClass(AST.IfElseStmt)
    def toTree(self):
        return Tree("IF", [self.rel_expr.toTree(), Tree("THEN", [self.if_stmt.toTree()]), Tree("ELSE", [self.else_stmt.toTree()])])

    @addToClass(AST.IfStmt)
    def toTree(self):
        return Tree("IF", [self.rel_expr.toTree(), Tree("THEN", [self.if_stmt.toTree()])])

    @addToClass(AST.WhileStmt)
    def toTree(self):
        return Tree("WHILE", [self.rel_expr.toTree(), self.while_stmt.toTree()])

    @addToClass(AST.ForStmt)
    def toTree(self):
        return Tree("FOR", [Tree(self.iter_variable), Tree("RANGE", [self.range_begin.toTree(), self.range_end.toTree()]), self.for_stmt.toTree()])

    @addToClass(AST.PrintStmt)
    def toTree(self):
        return Tree("PRINT", [self.print_stmt.toTree()])

    @addToClass(AST.PrintRecursive)
    def toTree(self):        
        return Tree("PRINT_ELEM", [self.print_rec.toTree(), self.print_expr.toTree()]) 
    
    @addToClass(AST.PrintExpr)
    def toTree(self):
        return self.print_expr.toTree()

    @addToClass(AST.Value)
    def toTree(self):
         return self.val.toTree()

    @addToClass(AST.ArithNumExpr)
    def toTree(self):
        return Tree(self.op, [self.left.toTree(), self.right.toTree()])

    @addToClass(AST.Variable)
    def toTree(self):
        return Tree(self.name)

    @addToClass(AST.IntNum)
    def toTree(self):
        return Tree(self.value)
        
    @addToClass(AST.FloatNum)
    def toTree(self):
        return Tree(self.value)

    @addToClass(AST.String)
    def toTree(self):
        return Tree(self.value)

    @addToClass(AST.AssignExpression)
    def toTree(self):
        return self.expression.toTree()

    @addToClass(AST.RelationExpression)
    def toTree(self):
        return self.expression.toTree()

    @addToClass(AST.MatrixExpression)
    def toTree(self):
        return self.expression.toTree()

    @addToClass(AST.UnaryExpression)
    def toTree(self):
        return Tree(self.op, [self.expression.toTree()])

    @addToClass(AST.MatrixNode)
    def toTree(self):
        return self.values.toTree()

    @addToClass(AST.GeneralExpression)
    def toTree(self):
        if self.special_op == "'":
             return Tree("TRANSPOSE", [self.expression.toTree()])
        else:
            return self.expression.toTree()

    @addToClass(AST.ArithMatExpr)
    def toTree(self):
        return Tree(self.div_op, [self.left.toTree(), self.right.toTree()])

    @addToClass(AST.DeclareExpr)
    def toTree(self):
        return Tree(self.op, [self.left.toTree(), self.right.toTree()])

    @addToClass(AST.UpdateExpr)
    def toTree(self):
        return Tree(self.assign_op, [self.left.toTree(), self.right.toTree()])

    @addToClass(AST.CompExpr)
    def toTree(self):
        return Tree(self.comp_op, [self.left.toTree(), self.right.toTree()])

    @addToClass(AST.MatrixRef)
    def toTree(self):
        return self.matrix_ref.toTree()

    @addToClass(AST.TabRef)
    def toTree(self):
        return self.tab_ref.toTree()

    @addToClass(AST.DoubleRef)
    def toTree(self):
        return Tree("REF", [Tree(self.id), self.row.toTree(), self.col.toTree()])

    @addToClass(AST.SingleRef)
    def toTree(self):
        return Tree("REF", [Tree(self.id), self.row.toTree()])

    @addToClass(AST.TabRefBoth)
    def toTree(self):
        return Tree("REF", [Tree(self.id), self.begin.toTree(), Tree(":"), self.end.toTree()])

    @addToClass(AST.TabRefEnd)
    def toTree(self):
        return Tree("REF", [Tree(self.id), Tree(":"), self.end.toTree()])

    @addToClass(AST.TabRefBegin)
    def toTree(self):
        return Tree("REF", [Tree(self.id), self.begin.toTree(), Tree(":")])

    @addToClass(AST.MatrixRowsNode)
    def toTree(self):
        return Tree("VECTOR", [row.toTree() for row in self.rows])

    @addToClass(AST.NumLineNode)
    def toTree(self):
        return Tree("VECTOR", [Tree(val) for val in self.num_line])

    @addToClass(AST.MatrixFuncs)
    def toTree(self):
        return Tree(self.fun, [Tree(self.value)])

    @addToClass(AST.Error)
    def toTree(self):
        return Tree("ERROR")