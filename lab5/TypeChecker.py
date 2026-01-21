import AST
from SymbolTable import *
from collections import defaultdict

ttype = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: None)))

# int - int entries
ttype['+']["int"]["int"] = "int"
ttype['-']["int"]["int"] = "int"
ttype['*']["int"]["int"] = "int"
ttype['/']["int"]["int"] = "float"
ttype['+=']["int"]["int"] = "int"
ttype['-=']["int"]["int"] = "int"
ttype['*=']["int"]["int"] = "int"
ttype['/=']["int"]["int"] = "float"
ttype['<']["int"]["int"] = "logic"
ttype['>']["int"]["int"] = "logic"
ttype['<=']["int"]["int"] = "logic"
ttype['>=']["int"]["int"] = "logic"
ttype['==']["int"]["int"] = "logic"
ttype['!=']["int"]["int"] = "logic"

# int - float entries
ttype['+']["int"]["float"] = "float"
ttype['-']["int"]["float"] = "float"
ttype['*']["int"]["float"] = "float"
ttype['/']["int"]["float"] = "float"
ttype['+=']["int"]["float"] = "float"
ttype['-=']["int"]["float"] = "float"
ttype['*=']["int"]["float"] = "float"
ttype['/=']["int"]["float"] = "float"
ttype['<']["int"]["float"] = "logic"
ttype['>']["int"]["float"] = "logic"
ttype['<=']["int"]["float"] = "logic"
ttype['>=']["int"]["float"] = "logic"
ttype['==']["int"]["float"] = "logic"
ttype['!=']["int"]["float"] = "logic"

# float - int entries
ttype['+']["float"]["int"] = "float"
ttype['-']["float"]["int"] = "float"
ttype['*']["float"]["int"] = "float"
ttype['/']["float"]["int"] = "float"
ttype['+=']["float"]["int"] = "float"
ttype['-=']["float"]["int"] = "float"
ttype['*=']["float"]["int"] = "float"
ttype['/=']["float"]["int"] = "float"
ttype['<']["float"]["int"] = "logic"
ttype['>']["float"]["int"] = "logic"
ttype['<=']["float"]["int"] = "logic"
ttype['>=']["float"]["int"] = "logic"
ttype['==']["float"]["int"] = "logic"
ttype['!=']["float"]["int"] = "logic"

# float - float entries
ttype['+']["float"]["float"] = "float"
ttype['-']["float"]["float"] = "float"
ttype['*']["float"]["float"] = "float"
ttype['/']["float"]["float"] = "float"
ttype['+=']["float"]["float"] = "float"
ttype['-=']["float"]["float"] = "float"
ttype['*=']["float"]["float"] = "float"
ttype['/=']["float"]["float"] = "float"
ttype['<']["float"]["float"] = "logic"
ttype['>']["float"]["float"] = "logic"
ttype['<=']["float"]["float"] = "logic"
ttype['>=']["float"]["float"] = "logic"
ttype['==']["float"]["float"] = "logic"
ttype['!=']["float"]["float"] = "logic"

# vector - vector entries
ttype['+=']["vector"]["vector"] = "vector"
ttype['-=']["vector"]["vector"] = "vector"
ttype['*=']["vector"]["vector"] = "vector"
ttype['/=']["vector"]["vector"] = "vector"

# special operations for vectors and mixed types
# "DOTADD"
ttype['.+']["vector"]["vector"] = "vector"
ttype['.+']["vector"]['int'] = "vector"
ttype['.+']["vector"]['float'] = "vector"
ttype['.+']["int"]["vector"] = "vector"
ttype['.+']["float"]["vector"] = "vector"

# "DOTSUB"
ttype['.-']["vector"]["vector"] = "vector"
ttype['.-']["vector"]["int"] = "vector"
ttype['.-']["vector"]["float"] = "vector"
ttype['.-']["int"]["vector"] = "vector"
ttype['.-']["float"]["vector"] = "vector"

# "DOTMUL"
ttype['.*']["vector"]["vector"] = "vector"
ttype['.*']["vector"]["int"] = "vector"
ttype['.*']["vector"]["float"] = "vector"
ttype['.*']["int"]["vector"] = "vector"
ttype['.*']["float"]["vector"] = "vector"

# "DOTDIV"
ttype['./']["vector"]["vector"] = "vector"
ttype['./']["vector"]["int"] = "vector"
ttype['./']["vector"]["float"] = "vector"
ttype['./']["int"]["vector"] = "vector"
ttype['./']["float"]["vector"] = "vector"

# other
ttype['\'']["vector"][None] = "vector"
ttype['-']["vector"][None] = "vector"
ttype['-']["int"][None] = "int"
ttype['-']["float"][None] = "float"
ttype['+']["string"]["string"] = "string"
ttype["*"]["string"]["int"] = "string"
ttype["*"]["int"]["string"] = "string"


class NodeVisitor(object):
    def visit(self, node):
        method = 'visit_' + node.__class__.__name__
        visitor = getattr(self, method, self.generic_visit)
        return visitor(node)

    # Called if no explicit visitor function exists for a node
    def generic_visit(self, node):
        if isinstance(node, list):
            for elem in node:
                self.visit(elem)
        else:
            for child in node.children:
                if isinstance(child, list):
                    for item in child:
                        if isinstance(item, AST.Node):
                            self.visit(item)
                elif isinstance(child, AST.Node):
                    self.visit(child)


class TypeChecker(NodeVisitor):
    def __init__(self):
        self.table = SymbolTable(None, "root")
        self.errors = []

    def visit_MultipleStmts(self, node):
        for stmt in node.stmts:
            self.visit(stmt)

    def visit_ControlStmt(self, node):
        scope = self.table

        while (scope.name != "root"):
            if (scope.name == "for_stmt" or scope.name == "while_stmt"):
                return
            
            scope = scope.parent

        self.errors.append(f"Błąd w linii {node.lineno}: `{node.control_stmt}` w złym miejscu!")

    def visit_StatementsSet(self, node):
        self.table = self.table.pushScope("stmts_set")
        self.visit(node.stmts)
        self.table = self.table.popScope()

    def visit_SpecificStmt(self, node):
        self.visit(node.specific_stmt)

    def visit_ReturnExpression(self, node):
        scope = self.table

        while scope.name != "root":
            if scope.name == "stmts_set":
                self.visit(node.expression)
                return
            
            scope = scope.parent

        self.errors.append(f"Błąd w linii {node.lineno}: `return` w złym miejscu!")
        self.visit(node.expression)

    def visit_IfElseStmt(self, node):
        self.visit(node.rel_expr)
        self.table = self.table.pushScope("if_stmt")
        self.visit(node.if_stmt)
        self.table = self.table.popScope()

        self.table = self.table.pushScope("else_stmt")
        self.visit(node.else_stmt)
        self.table = self.table.popScope()

    def visit_IfStmt(self, node):
        self.visit(node.rel_expr)
        self.table = self.table.pushScope("if_stmt")
        self.visit(node.if_stmt)
        self.table = self.table.popScope()

    def visit_WhileStmt(self, node):
        self.visit(node.rel_expr)
        self.table = self.table.pushScope("while_stmt")
        self.visit(node.while_stmt)
        self.table = self.table.popScope()

    def visit_ForStmt(self, node):
        self.table = self.table.pushScope("for_stmt")
        var = VariableSymbol(node.iter_variable, "int")
        self.table.put(node.iter_variable, var)

        self.visit(node.range_begin)
        self.visit(node.range_end)
        self.visit(node.for_stmt)

        self.table = self.table.popScope()

    def visit_PrintStmt(self, node):
        self.visit(node.print_stmt)

    def visit_PrintRecursive(self, node):
        self.visit(node.print_rec)
        self.visit(node.print_expr)

    def visit_PrintExpr(self, node):
        self.visit(node.print_expr)

    def visit_Value(self, node):
        return self.visit(node.val)
    
    def visit_ArithNumExpr(self, node):
        # alternative usage, requires definition of 'accept' method in class 'Node'
        # type1 = node.left.accept(self)
        # type2 = node.right.accept(self)
        type1 = self.visit(node.left)
        type2 = self.visit(node.right)
        op = node.op
        type = ttype[op][type1][type2]

        if type is None:
            self.errors.append(f"Błąd w linii {node.lineno}: działanie na niekompatybilnych typach danych: {type1} i {type2}!")
            return

        return type

    def visit_Variable(self, node):
        var = self.table.get(node.name)

        if var is None:
            self.errors.append(f"Błąd w linii {node.lineno}: nie rozpoznano zmiennej `{node.name}`!")
            return

        return var.type

    def visit_IntNum(self, node):
        return "int"
    
    def visit_AssignExpression(self, node):
        self.visit(node.expression)

    def visit_RelationExpression(self, node):
        return self.visit(node.expression)
    
    def visit_MatrixExpression(self, node):
        return self.visit(node.expression)

    def visit_UnaryExpression(self, node):
        op = node.op
        type1 = self.visit(node.expression)
        type = ttype[op][type1][None]

        return type

    def visit_MatrixNode(self, node):
        self.visit(node.values)

    def visit_GeneralExpression(self, node):
        return self.visit(node.expression)
    
    def visit_ArithMatExpr(self, node):
        type1 = self.visit(node.left)
        type2 = self.visit(node.right)
        op = node.div_op
        type = ttype[op][type1][type2]

        if type is None:
            self.errors.append(f"Błąd w linii {node.lineno}: działanie na niekompatybilnych typach danych: {type1} i {type2}!")
            return

        if type != "" and type1 == "vector" and type2 == "vector":
            if isinstance(node.left, AST.GeneralExpression):
                m1 = self.table.get(node.left.expression.val.name)
            else:
                m1 = self.table.get(node.left.val.name)
            
            if isinstance(node.right, AST.GeneralExpression):
                m2 = self.table.get(node.right.expression.val.name)
            else:
                m2 = self.table.get(node.right.val.name)

            if (m1.size != m2.size or m1.dimension != m2.dimension) and op in [".+", ".-", "./"]:
                self.errors.append(f"Błąd w linii {node.lineno}: nie można wykonywać operacji `{op}` na macierzach o różnych wymiarach!")
                return
            
            if m1.size[1] != m2.size[0] and op == ".*":
                self.errors.append(f"Błąd w linii {node.lineno}: nie można wykonywać operacji `{op}` na macierzach o niekompatybilnych wymiarach!")
                return

        return type

    def visit_DeclareExpr(self, node):
        type = self.visit(node.right)

        if isinstance(node.left, AST.TabRef) or isinstance(node.left, AST.MatrixRef):
            self.visit(node.left)
            return
        
        name = node.left.name
        var_type = ""
        size = [0, 0]
        dimension = 0  # zakładamy maksymalnie dwa wymiary

        # odpowiada za inicjalizację/nadpisanie macierzą
        if isinstance(node.right, AST.MatrixNode):
            var_type = "vector"
            row_len = -1

            if isinstance(node.right.values, AST.MatrixRowsNode):
                dimension = 2

                for row in node.right.values.rows:
                    size[0] += 1

                    if (row_len == -1):
                        row_len = len(row.num_line)
                    elif (len(row.num_line) != row_len):
                        self.errors.append(f"Błąd w linii {node.lineno}: różne długości wierszy w macierzy!")
                        return

                size[1] = len(node.right.values.rows[0].num_line)
            elif isinstance(node.right.values, AST.NumLineNode):
                dimension = 1
                size[0] = len(node.right.values.num_line)
                size[1] = 1

        # odpowiada za inicjalizację/nadpisanie wyrażeniem
        elif isinstance(node.right, AST.ArithNumExpr) or isinstance(node.right, AST.ArithMatExpr):
            var_type = type

            if type == "vector":
                pass

        # odpowiada za inicjalizację/nadpisanie pojedynczą zmienną lub wartością
        elif isinstance(node.right, AST.Value):
            var_type = type

        # odpowiada za inicjalizację/nadpisanie funkcją do macierzy
        elif isinstance(node.right.expression, AST.MatrixFuncs):
            var_type = "vector"
            arg = node.right.expression.value
            size = [arg, arg]
            dimension = 2

            if arg < 0:
                return

        elif isinstance(node.right, AST.GeneralExpression):
            matrix = self.table.get(node.right.expression.val.name)

            if matrix != None:
                size = matrix.size
                var_type = matrix.type
                dimension = matrix.dimension

        if var_type == "":
            var_type = type

        if var_type == "vector":
            var = VectorSymbol(name, size, var_type, dimension)
        else:
            var = VariableSymbol(name, var_type)

        if var_type != None:
            self.table.put(name, var)
            self.visit(node.left)

    def visit_UpdateExpr(self, node):
        type1 = self.visit(node.left)
        type2 = self.visit(node.right)
        op = node.assign_op
        type = ttype[op][type1][type2]

        if type is None:
            self.errors.append(f"Błąd w linii {node.lineno}: działanie na niekompatybilnych typach danych: {type1} i {type2}!")
            return

        return type

    def visit_CompExpr(self, node):
        type1 = self.visit(node.left)
        type2 = self.visit(node.right)
        op = node.comp_op
        type = ttype[op][type1][type2]

        if type is None:
            self.errors.append(f"Błąd w linii {node.lineno}: działanie na niekompatybilnych typach danych: {type1} i {type2}!")
            return

        return type

    def visit_MatrixRef(self, node):
        self.visit(node.matrix_ref)

    def visit_TabRef(self, node):
        self.visit(node.tab_ref)

    def visit_DoubleRef(self, node):
        self.visit(node.row)
        self.visit(node.col)
        vector = self.table.get(node.id)

        if not vector:
            self.errors.append(f"Błąd w linii {node.lineno}: nie rozpoznano zmiennej `{node.id}`!")
            return

        if not isinstance(vector, VectorSymbol):
            self.errors.append(f"Błąd w linii {node.lineno}: zły typ zmiennej!")
            return

        if vector.dimension < 2:
            self.errors.append(f"Błąd w linii {node.lineno}: za dużo argumentów!")
            return

        if node.row.value >= vector.size[0] or node.col.value >= vector.size[1]:
            self.errors.append(f"Błąd w linii {node.lineno}: zły wymiar macierzy!")
            return

        return "int"

    def visit_SingleRef(self, node):
        self.visit(node.row)
        vector = self.table.get(node.id)

        if not vector:
            self.errors.append(f"Błąd w linii {node.lineno}: nie rozpoznano zmiennej `{node.id}`!")
            return

        if not isinstance(vector, VectorSymbol):
            self.errors.append(f"Błąd w linii {node.lineno}: zły typ zmiennej!")
            return

        if node.row.value >= vector.size[0]:
            self.errors.append(f"Błąd w linii {node.lineno}: zły wymiar macierzy!")
            return

        return "vector"

    def visit_TabRefBoth(self, node):
        self.visit(node.begin)
        self.visit(node.end)
        vector = self.table.get(node.id)

        if not vector:
            self.errors.append(f"Błąd w linii {node.lineno}: nie rozpoznano zmiennej `{node.id}`!")
            return

        if not isinstance(vector, VectorSymbol):
            self.errors.append(f"Błąd w linii {node.lineno}: zły typ zmiennej!")
            return

        if node.end.value > vector.size[0] or node.begin.value > node.end.value or node.begin.value < 0:
            self.errors.append(f"Błąd w linii {node.lineno}: zły wymiar tablicy!")
            return

        return "vector"

    def visit_TabRefEnd(self, node):
        self.visit(node.end)
        vector = self.table.get(node.id)

        if not vector:
            self.errors.append(f"Błąd w linii {node.lineno}: nie rozpoznano zmiennej `{node.id}`!")
            return

        if not isinstance(vector, VectorSymbol):
            self.errors.append(f"Błąd w linii {node.lineno}: zły typ zmiennej!")
            return

        if node.end.value > vector.size[0] or node.end.value < 0:
            self.errors.append(f"Błąd w linii {node.lineno}: zły wymiar tablicy!")
            return

        return "vector"

    def visit_TabRefBegin(self, node):
        self.visit(node.begin)
        vector = self.table.get(node.id)

        if not vector:
            self.errors.append(f"Błąd w linii {node.lineno}: nie rozpoznano zmiennej `{node.id}`!")
            return

        if not isinstance(vector, VectorSymbol):
            self.errors.append(f"Błąd w linii {node.lineno}: zły typ zmiennej!")
            return

        if node.begin.value > vector.size[0] or node.begin.value < 0:
            self.errors.append(f"Błąd w linii {node.lineno}: zły wymiar tablicy!")
            return

        return "vector"
    
    def visit_MatrixRowsNode(self, node):
        for value in node.rows:
            self.visit(value)

    def visit_NumLineNode(self, node):
        pass

    def visit_MatrixFuncs(self, node):
        if node.value < 0:
            self.errors.append(f"Błąd w linii {node.lineno}: argument dla funkcji `{node.fun}` mniejszy lub równy zero!")
            return

        return "vector"

    def visit_FloatNum(self, node):
        return "float"

    def visit_String(self, node):
        return "string"