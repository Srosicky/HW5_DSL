# Need to install lark via pip
# pip install lark
# Note for me this puts it into the homebrew install of python,
#  so I need to run with the following rather than python3:
# /opt/homebrew/bin/python3.10 expressionParser.py
# otherwise it would just be: python expressionParser.py


text = """
10 + 2 * (3 - 4)
"""

from lark import Lark

# Use LALR rather than Earley
# LALR works best with left recursive grammars
parser = Lark.open("expressionGrammar.lark", parser="lalr")
parseTree = parser.parse(text)
print(parseTree)
print(parseTree.pretty())
# The tree is a parse tree not an AST


# Now define an evaluator for the parse tree
# Note that we need to define 2 behaviors for things with 2 rules
# With an AST this would have already been abstracted away
def eval(pt):
    if pt.data == "expr":
        # An expr should have 3 children: left addop|subop right
        # or 1 child: term
        if len(pt.children) == 1:
            return (eval(pt.children[0]))
        else:
            if pt.children[1].data == "addop":
                return (eval(pt.children[0]) + eval(pt.children[2]))
            else:
                return (eval(pt.children[0]) - eval(pt.children[2]))

    elif pt.data == "term":
        # A term should have 3 children: left multop|divop right
        # or 1 child: factor
        if len(pt.children) == 1:
            return (eval(pt.children[0]))
        else:
            if pt.children[1].data == "multop":
                return (eval(pt.children[0]) * eval(pt.children[2]))
            else:
                return (eval(pt.children[0]) / eval(pt.children[2]))

    elif pt.data == "factor":
        # A factor should have either 3 children leftparen, expr, rightparen
        # or 1 child: the NUMBER
        if len(pt.children) == 3:
            return (eval(pt.children[1]))
        else:
            return (int(pt.children[0])) # Convert to a number

    else:
        print("!!!!!ERROR!!!!!")

# The start node has only 1 child so just eval this directly
e1 = eval(parseTree.children[0])
print("ParseTree Evaluator Result", e1)


# Now turn the parseTree into a AST using a Transformer
# We want an AST like the following one from Haskell:
#  Add (Val 10) (Mul (Val 2) (Sub (Val 3) (Val 4)))

# Use a Lark Transformer to do this
# It uses a Visitor Pattern and does the leaf nodes first
# Note that the visitor patter visits every node in the parseTree
# and calls the function that matches the parseTree type
# Then when building the AST, it basically replaces that branch
# of the parseTree with the returned AST node (in a new tree)
from lark import Transformer

class ExpressionTransformer(Transformer):
    # Terminals (like NUMBER) receive the Token object
    def NUMBER(self, n):
        return ("val", int(n))

    # Rules receive a list of their children's results

    def start(self, children):
        return children[0]
    
    def expr(self, children):
        if len(children) == 1:
            return children[0]
        # children = [left_val, addop|subop, right_val]
        # So make the addop|subop the top of the subtree
        # Use the .value part to pull the name out of the Token
        return (children[1].data.value, children[0], children[2])

    def term(self, children):
        if len(children) == 1:
            return children[0]
        return (children[1].data.value, children[0], children[2])

    def factor(self, children):
        if len(children) == 1:
            return children[0]
        return (children[1]) # removes leftparen and rightparen


# Note that the AST is simply a tuple (and not a lark tree)
ast = ExpressionTransformer().transform(parseTree)
print(ast)

# And finally an evaluator for the AST
# This could have been done as a visitor using the intrepter lark class
# but I think it is more informative to do it as a simple recursive function
def evalAST(ast):
    if ast[0] == "val":
        return ast[1]
    elif ast[0] == "addop":
        return evalAST(ast[1]) + evalAST(ast[2])
    elif ast[0] == "subop":
        return evalAST(ast[1]) - evalAST(ast[2])
    elif ast[0] == "multop":
        return evalAST(ast[1]) * evalAST(ast[2])
    elif ast[0] == "divop":
        return evalAST(ast[1]) // evalAST(ast[2])
    else:
        return "ERROR"
    
e2 = evalAST(ast)
print("AST Evaluator Result", e2)