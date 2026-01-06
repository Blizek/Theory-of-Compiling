import AST


def addToClass(cls):
    def decorator(func):
        setattr(cls, func.__name__, func)
        return func

    return decorator


class TreePrinter:
    @addToClass(AST.Node)
    def printTree(self, indent=0):
        raise Exception("printTree not defined in class " + self.__class__.__name__)

    @addToClass(AST.MultipleStmts)
    def printTree(self, indent=0):
        for stmt in self.stmts:
            stmt.printTree(indent)

    @addToClass(AST.ControlStmt)
    def printTree(self, indent=0):
        print("|  " * indent + (self.control_stmt).upper())

    @addToClass(AST.StatementsSet)
    def printTree(self, indent=0):
        self.stmts.printTree(indent)

    @addToClass(AST.SpecificStmt)
    def printTree(self, indent=0):
        self.specific_stmt.printTree(indent)

    @addToClass(AST.ReturnExpression)
    def printTree(self, indent=0):
        print("|  " * indent + "RETURN")
        self.expression.printTree(indent + 1)

    @addToClass(AST.IfElseStmt)
    def printTree(self, indent=0):
        print("|  " * indent + "IF")
        self.rel_expr.printTree(indent + 1)
        print("|  " * indent + "THEN")
        self.if_stmt.printTree(indent + 1)
        print("|  " * indent + "ELSE")
        self.else_stmt.printTree(indent + 1)

    @addToClass(AST.IfStmt)
    def printTree(self, indent=0):
        print("|  " * indent + "IF")
        self.rel_expr.printTree(indent + 1)
        print("|  " * indent + "THEN")
        self.if_stmt.printTree(indent + 1)

    @addToClass(AST.WhileStmt)
    def printTree(self, indent=0):
        print("|  " * indent + "WHILE")
        self.rel_expr.printTree(indent + 1)
        self.while_stmt.printTree(indent + 1)

    @addToClass(AST.ForStmt)
    def printTree(self, indent=0):
        print("|  " * indent + "FOR")
        print("|  " * (indent + 1) + str(self.iter_variable))
        print("|  " * (indent + 1) + "RANGE")
        self.range_begin.printTree(indent + 2)
        self.range_end.printTree(indent + 2)
        self.for_stmt.printTree(indent + 1)

    @addToClass(AST.PrintStmt)
    def printTree(self, indent=0):
        print("|  " * indent + "PRINT")
        self.print_stmt.printTree(indent + 1)

    @addToClass(AST.PrintRecursive)
    def printTree(self, indent=0):
        self.print_rec.printTree(indent)
        self.val.printTree(indent)

    @addToClass(AST.Value)
    def printTree(self, indent=0):
        self.val.printTree(indent)

    @addToClass(AST.Variable)
    def printTree(self, indent=0):
        print("|  " * indent + self.name)

    @addToClass(AST.IntNum)
    def printTree(self, indent=0):
        print("|  " * indent + str(self.value))

    @addToClass(AST.AssignExpression)
    def printTree(self, indent=0):
        self.expression.printTree(indent)

    @addToClass(AST.DeclareExpr)
    def printTree(self, indent=0):
        print("|  " * indent + self.op)
        self.left.printTree(indent + 1)
        self.right.printTree(indent + 1)

    @addToClass(AST.RelationExpression)
    def printTree(self, indent=0):
        self.expression.printTree(indent)

    @addToClass(AST.MatrixExpression)
    def printTree(self, indent=0):
        self.expression.printTree(indent)

    @addToClass(AST.UnaryExpression)
    def printTree(self, indent=0):
        print("|  " * indent + self.op)
        self.expression.printTree(indent + 1)

    @addToClass(AST.MatrixRowsNode)
    def printTree(self, indent=0):
        print("|  " * indent + "VECTOR")
        for value in self.rows:
            value.printTree(indent + 1)

    @addToClass(AST.NumLineNode)
    def printTree(self, indent=0):
        print("|  " * indent + "VECTOR")
        for value in self.num_line:
            print(f"{'|  ' * (indent + 1)}{value}")

    @addToClass(AST.GeneralExpression)
    def printTree(self, indent=0):
        print("|  " * indent + "TRANSPOSE")
        self.expression.printTree(indent + 1)

    @addToClass(AST.BinExpr)
    def printTree(self, indent=0):
        print("|  " * indent + self.op)
        self.left.printTree(indent + 1)
        self.right.printTree(indent + 1)

    @addToClass(AST.MatrixRef)
    def printTree(self, indent=0):
        self.matrix_ref.printTree(indent)

    @addToClass(AST.TabRef)
    def printTree(self, indent=0):
        self.tab_ref.printTree(indent)

    @addToClass(AST.DoubleRef)
    def printTree(self, indent=0):
        print("|  " * indent + "REF")
        print("|  " * (indent + 1) + self.id)
        self.row.printTree(indent + 1)
        self.col.printTree(indent + 1)

    @addToClass(AST.SingleRef)
    def printTree(self, indent=0):
        print("|  " * indent + "REF")
        self.row.printTree(indent + 1)

    @addToClass(AST.TabRefBoth)
    def printTree(self, indent=0):
        print("|  " * indent + "REF")
        print("|  " * (indent + 1) + self.id)
        self.begin.printTree(indent + 1)
        print("|  " * (indent + 1) + ":")
        self.end.printTree(indent + 1)

    @addToClass(AST.TabRefEnd)
    def printTree(self, indent=0):
        print("|  " * indent + "REF")
        print("|  " * (indent + 1) + self.id)
        print("|  " * (indent + 1) + ":")
        self.end.printTree(indent + 1)

    @addToClass(AST.TabRefBegin)
    def printTree(self, indent=0):
        print("|  " * indent + "REF")
        print("|  " * (indent + 1) + self.id)
        self.begin.printTree(indent + 1)
        print("|  " * (indent + 1) + ":")

    @addToClass(AST.MatrixFuncs)
    def printTree(self, indent=0):
        print("|  " * indent + self.fun)
        print("|  " * (indent + 1) + str(self.value))

    @addToClass(AST.FloatNum)
    def printTree(self, indent=0):
        print("|  " * indent + str(self.value))

    @addToClass(AST.String)
    def printTree(self, indent=0):
        print("|  " * indent + self.value)

    @addToClass(AST.MatrixNode)
    def printTree(self, indent=0):
        self.values.printTree(indent)

    @addToClass(AST.Error)
    def printTree(self, indent=0):
        pass
        # fill in the body