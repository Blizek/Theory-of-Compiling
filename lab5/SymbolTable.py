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
    # parent scope and symbol table name
    def __init__(self, parent, name):
        self.symbol_table = {}
        self.name = name
        self.parent = parent # widzę parent jako wskaźnik do tablicy symboli dla poprzedniego scope'a

    # put variable symbol or fundef under <name> entry
    def put(self, name, symbol):
        self.symbol_table[name] = symbol

    # get variable symbol or fundef from <name> entry
    def get(self, name):
        result = self.symbol_table.get(name)

        if result is None and self.parent is not None:
            result = self.parent.get(name)

        return result

    def pushScope(self, name):
        # dla nowo dodanej tablicy obecna jest rodzicem
        new_table = SymbolTable(self, name)
        return new_table

    def popScope(self):
        # "przywracam" poprzednią tablicę 
        prev_table = self.parent
        return prev_table