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
        # 1. Rekurencyjne odwiedzenie lewego i prawego poddrzewa, aby uzyskać wartości operandów
        left = self.visit(node.left)
        right = self.visit(node.right)
        
        # 2. Pobranie operatora i odpowiadającej mu funkcji z mapowania (np. dodawanie, odejmowanie)
        op = node.div_op
        func = operations[op]

        # --- LOGIKA BROADCASTINGU (Dopasowanie wymiarów) ---
        # Jeśli lewa strona jest wektorem, a prawa macierzą - rozszerzamy lewą stronę,
        # by pasowała strukturą do macierzy (kopiowanie wartości wierszy).
        if not all(isinstance(el, list) for el in left) and all(isinstance(el, list) for el in right):
            left = [[l] * len(right[0]) for l in left]
            
        # Analogicznie: jeśli prawa strona jest "płaska", a lewa to macierz - rozszerzamy prawą.
        elif not all(isinstance(el, list) for el in right) and all(isinstance(el, list) for el in left):
            right = [[r] * len(left[0]) for r in right]

        # --- OBSŁUGA MNOŻENIA (Specjalny przypadek operatora '.*') ---
        if op == '.*':
            # Jeśli oba operandy są wektorami (listami 1D) - wykonaj mnożenie element po elemencie
            if not all(isinstance(el, list) for el in left) and not all(isinstance(el, list) for el in right):
                return [l * r for l, r in zip(left, right)]

            # Klasyczne mnożenie macierzy (Matrix Multiplication) dla struktur 2D
            # Inicjalizacja macierzy wynikowej zerami o wymiarach [wiersze_lewej x kolumny_prawej]
            result = [[0. for _ in range(len(right[0]))] for _ in range(len(left))]

            # Potrójna pętla - standardowy algorytm mnożenia macierzy: C[i][j] = Σ (A[i][k] * B[k][j])
            for i in range(len(left)): # po wierszach lewej macierzy
                for j in range(len(right[0])): # po kolumnach prawej macierzy
                    suma = 0
                    for k in range(len(left[0])): # iloczyn skalarny wiersza i kolumny
                        suma += left[i][k] * right[k][j]
                    result[i][j] = suma

            return result
            
        # --- POZOSTAŁE OPERACJE (np. +, -, /) ---
        else:
            # Dla wektorów: wykonaj operację element po elemencie
            if not all(isinstance(el, list) for el in left) and not all(isinstance(el, list) for el in right):
                return [func(l, r) for l, r in zip(left, right)]

            # Dla macierzy: wykonaj operację element po elemencie w strukturze 2D
            return [[func(l, r) for l, r in zip(lrow, rrow)] for lrow, rrow in zip(left, right)]

    @when(AST.DeclareExpr)
    def visit(self, node):
        # --- PRZYPADEK 1: Przypisanie do zwykłej zmiennej (np. x = 5) ---
        if isinstance(node.left, AST.Variable):
            name = node.left.name
            value = self.visit(node.right) # Obliczamy wartość wyrażenia po prawej stronie

            # Sprawdzamy, czy zmienna już istnieje w pamięci
            if self.memory_stack.get(name) is None:
                self.memory_stack.insert(name, value) # Nowa zmienna -> dodaj do stosu
            else:
                self.memory_stack.set(name, value)    # Istniejąca zmienna -> aktualizuj wartość
                
        # --- PRZYPADEK 2: Przypisanie do elementu macierzy lub jej wycinka (np. A[1,2] = 5 lub A[1:5] = 0) ---
        else:
            # Zakładamy, że node.left to operacja indeksowania, która zwraca nazwę i listę indeksów
            name, indices = self.visit(node.left)
            matrix = self.memory_stack.get(name) # Pobieramy macierz z pamięci
            value = self.visit(node.right)       # Obliczamy wartość do przypisania

            # A. OBSŁUGA ZAKRESU (Slicing) - np. A[1:5] = value
            # Logika dla 3 elementów w 'indices' sugeruje konstrukcję [początek, koniec, flaga_zakresu]
            if len(indices) == 3:
                begin = 0 if indices[0] is None else indices[0]
                end = len(matrix) if indices[1] is None else indices[1]

                # Wypełniamy wybrany zakres wierszy nową wartością
                for i in range(begin, end):
                    matrix[i] = value
                    
            # B. PRZYPISANIE DO KONKRETNEJ KOMÓRKI 2D - np. A[i, j] = value
            elif len(indices) == 2:
                matrix[indices[0]][indices[1]] = value
                
            # C. PRZYPISANIE DO KONKRETNEGO WIERSZA / ELEMENTU 1D - np. A[i] = value
            else:
                matrix[indices[0]] = value

            # Zaktualizuj zmodyfikowaną macierz w pamięci
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
        generators = {
            "zeros": lambda n: [[0. for _ in range(n)] for _ in range(n)],
            "ones":  lambda n: [[1. for _ in range(n)] for _ in range(n)],
            "eye":   lambda n: [[1. if i == j else 0. for j in range(n)] for i in range(n)]
        }

        matrix_func = generators.get(node.fun)

        if matrix_func:
            return matrix_func(node.value)
        
        raise ValueError(f"Nieznana funkcja macierzowa: {node.fun}")

    @when(AST.FloatNum)
    def visit(self, node):
        return node.value

    @when(AST.String)
    def visit(self, node):
        return node.value[1:-1]  

    @when(AST.Error)
    def visit(self, node):
        pass