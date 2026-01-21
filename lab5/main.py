import sys
from scanner import Scanner
from parser import Mparser
from TypeChecker import TypeChecker
from Interpreter import Interpreter
import TreePrinter

if __name__ == '__main__':
    try:
        filename = sys.argv[1] if len(sys.argv) > 1 else "examples/example.txt"
        file = open(filename, "r")
    except IOError:
        print("Cannot open {0} file".format(filename))
        sys.exit(0)

    text = file.read()
    lexer = Scanner()
    parser = Mparser()
    ast = parser.parse(lexer.tokenize(text))

    # Below code shows how to use visitor
    if ast is not None:
        print("Abstract syntax tree:")
        print(ast.printTree())
        print()
        
        typeChecker = TypeChecker()   
        typeChecker.visit(ast) # or alternatively ast.accept(typeChecker)

        if len(typeChecker.errors) > 0:
            print("Semantic analysis failed! Errors:")

            for error in typeChecker.errors:
                print(error)
        else:
            print("Interpreting the program:")
            interpreter = Interpreter()
            interpreter.visit(ast)
            # in future
            # ast.accept(OptimizationPass1())
            # ast.accept(OptimizationPass2())
            # ast.accept(CodeGenerator())