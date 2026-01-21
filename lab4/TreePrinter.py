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

    @addToClass(AST.Program)
    def toTree(self):
        return self.instructions.toTree()

    @addToClass(AST.Instructions)
    def toTree(self):
        return Tree(None, [instr.toTree() for instr in self.instructions])

    @addToClass(AST.BinExpr)
    def toTree(self):
        return Tree(self.op, [self.left.toTree(), self.right.toTree()])

    @addToClass(AST.RelExpr)
    def toTree(self):
        return Tree(self.op, [self.left.toTree(), self.right.toTree()])

    @addToClass(AST.Assignment)
    def toTree(self):
        return Tree(self.op, [self.left.toTree(), self.right.toTree()])

    @addToClass(AST.If)
    def toTree(self):
        children = [self.condition.toTree(), Tree("THEN", [self.then_block.toTree()])]
        if self.else_block:
            children.append(Tree("ELSE", [self.else_block.toTree()]))
        return Tree("IF", children)

    @addToClass(AST.While)
    def toTree(self):
        return Tree("WHILE", [self.condition.toTree(), self.body.toTree()])

    @addToClass(AST.For)
    def toTree(self):
        return Tree("FOR", [self.var.toTree(), self.range.toTree(), self.body.toTree()])

    @addToClass(AST.Range)
    def toTree(self):
        return Tree("RANGE", [self.start.toTree(), self.end.toTree()])

    @addToClass(AST.Break)
    def toTree(self):
        return Tree("BREAK")

    @addToClass(AST.Continue)
    def toTree(self):
        return Tree("CONTINUE")

    @addToClass(AST.Return)
    def toTree(self):
        return Tree("RETURN", [self.expr.toTree()])

    @addToClass(AST.Print)
    def toTree(self):
        return Tree("PRINT", [val.toTree() for val in self.values])

    @addToClass(AST.IntNum)
    def toTree(self):
        return Tree(self.value)

    @addToClass(AST.FloatNum)
    def toTree(self):
        return Tree(self.value)

    @addToClass(AST.String)
    def toTree(self):
        return Tree(f'"{self.value}"')

    @addToClass(AST.Variable)
    def toTree(self):
        return Tree(self.name)

    @addToClass(AST.VectorElement)
    def toTree(self):
        return Tree("REF", [Tree(self.name), Tree(self.index)])

    @addToClass(AST.MatrixElement)
    def toTree(self):
        return Tree("REF", [Tree(self.name), Tree(self.row), Tree(self.col)])

    @addToClass(AST.Matrix)
    def toTree(self):
        return Tree("VECTOR", [row.toTree() for row in self.rows])

    @addToClass(AST.Vector)
    def toTree(self):
        return Tree("VECTOR", [elem.toTree() for elem in self.elements])

    @addToClass(AST.MatrixFunction)
    def toTree(self):
        return Tree(self.name, [self.size.toTree()])

    @addToClass(AST.UnaryMinus)
    def toTree(self):
        return Tree("-", [self.expr.toTree()])

    @addToClass(AST.Transposition)
    def toTree(self):
        return Tree("TRANSPOSE", [self.expr.toTree()])