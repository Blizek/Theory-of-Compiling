class Symbol(object):
    pass


class VariableSymbol(Symbol):
    def __init__(self, name, type):
        self.name = name
        self.type = type


class VectorSymbol(Symbol):
    def __init__(self, name, size, type, dimension):
        self.name = name
        self.size = size
        self.type = type
        self.dimension = dimension


class SymbolTable(object):
    def __init__(self, parent, name):
        self.symbol_table = {}
        self.name = name
        self.counter = 0
        self.parent = parent

    def put(self, name, symbol):
        self.symbol_table[name] = symbol

    def get(self, name):
        result = self.symbol_table.get(name)
        if result is None and self.parent is not None:
            result = self.parent.get(name)

        return result

    def pushScope(self, name):
        new_table = SymbolTable(self, name)

        return new_table

    def popScope(self):
        prev_table = self.parent

        return prev_table