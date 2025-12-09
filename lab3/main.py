import sys
from scanner import Scanner
from parser import Mparser
import TreePrinter

def main():
    if len(sys.argv) < 2:
        print("Usage: python main.py <input_file>")
        sys.exit(1)
    
    filename = sys.argv[1]
    
    try:
        with open(filename, 'r') as file:
            text = file.read()
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found")
        sys.exit(1)
    
    lexer = Scanner()
    parser = Mparser()
    
    try:
        ast = parser.parse(lexer.tokenize(text))
        if ast is not None:
            tree_output = ast.printTree()

            with open('result.m', 'w') as output_file: output_file.write(tree_output)
        
    except Exception as e:
        print(f"Error during parsing: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()