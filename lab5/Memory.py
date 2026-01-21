class Memory:
    def __init__(self, name): # memory name
        self.name = name
        self.memory = {}

    def has_key(self, name): # variable name
        return name in self.memory.keys()

    def get(self, name): # gets from memory current value of variable <name>
        return self.memory.get(name)

    def put(self, name, value): # puts into memory current value of variable <name>
        self.memory[name] = value


class MemoryStack:                                                                       
    def __init__(self, memory = None): # initialize memory stack with memory <memory>
        self.memory_stack = [memory] if memory is not None else []

    def get(self, name): # gets from memory stack current value of variable <name>
        for i in range(len(self.memory_stack) - 1, -1, -1):
            if self.memory_stack[i].has_key(name):
                return self.memory_stack[i].get(name)

    def insert(self, name, value): # inserts into memory stack variable <name> with value <value>
        self.memory_stack[-1].put(name, value)

    def set(self, name, value): # sets variable <name> to value <value>
        for i in range(len(self.memory_stack) - 1, -1, -1):
            if self.memory_stack[i].has_key(name):
                self.memory_stack[i].put(name, value)

    def push(self, memory): # pushes memory <memory> onto the stack
        self.memory_stack.append(memory)

    def pop(self): # pops the top memory from the stack
        self.memory_stack.pop()