from lark import Lark
from classes import DrawingTransformer, DrawingPen
from helpers import evaluate_program

# load in text file
with open("/Users/sophiarosicky/Desktop/COMP 3351/Homeworks/HW5_DSL/instructions.txt", "r") as f:
    text = f.read()

# parse the instructions and generate the corresponding parse tree
parser = Lark.open("/Users/sophiarosicky/Desktop/COMP 3351/Homeworks/HW5_DSL/grammar.lark", parser="lalr")
parse_tree = parser.parse(text)
print(parse_tree.pretty())

# transform the parse three into AST and display
ast = DrawingTransformer().transform(parse_tree)
print(ast)

# evaluate the program
pen = DrawingPen()
evaluate_program(ast, pen)