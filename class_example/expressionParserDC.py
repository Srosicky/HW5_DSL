# Need to install lark via pip
# pip install lark
# Note for me this puts it into the homebrew install of python,
#  so I need to run with the following rather than python3:
# /opt/homebrew/bin/python3.10 expressionParser.py
# otherwise it would just be: python expressionParser.py

# This is the version where the AST nodes are dataclasses rather than tuples
# This is probably a closer match to the Haskell version where we had Node types for AST


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

# Will will use the dataclass decorator that adds simple
#   constructors, equality, and string functions for each class
#   Basically, everything you would need for a class that just held
#     but not processed data
from dataclasses import dataclass
from typing import Union

@dataclass
class Node:
    pass

@dataclass
class ValNode(Node):
    value: int

@dataclass
class BinaryOpNode(Node):
    left: Node
    right: Node

@dataclass
class AddNode(BinaryOpNode): pass

@dataclass
class SubNode(BinaryOpNode): pass

@dataclass
class MultNode(BinaryOpNode): pass

@dataclass
class DivNode(BinaryOpNode): pass



# Use a Lark Transformer to do this
# It uses a Visitor Pattern
from lark import Transformer

class ExpressionTransformer(Transformer):
    def NUMBER(self, n):
        return ValNode(int(n))

    def start(self, children):
        return children[0]
    
    def expr(self, children):
        if len(children) == 1:
            return children[0]
        
        # Determine operator class based on the rule data
        op_map = {'addop': AddNode, 'subop': SubNode}
        op_class = op_map[children[1].data]
        return op_class(children[0], children[2])

    def term(self, children):
        if len(children) == 1:
            return children[0]
        
        op_map = {'multop': MultNode, 'divop': DivNode}
        op_class = op_map[children[1].data]
        return op_class(children[0], children[2])

    def factor(self, children):
        if len(children) == 1:
            return children[0]
        return children[1] # paren version
    


# Note that the AST is simply a tuple (and not a lark tree)
ast = ExpressionTransformer().transform(parseTree)
print(ast)



# And finally an evaluator for the AST
def evalAST(node: Node):
    if isinstance(node, ValNode):
        return node.value
    elif isinstance(node, AddNode):
        return evalAST(node.left) + evalAST(node.right)
    elif isinstance(node, SubNode):
        return evalAST(node.left) - evalAST(node.right)
    elif isinstance(node, MultNode):
        return evalAST(node.left) * evalAST(node.right)
    elif isinstance(node, DivNode):
        return evalAST(node.left) // evalAST(node.right)
    raise ValueError(f"Unknown node type: {type(node)}")

    
e2 = evalAST(ast)
print("AST Evaluator Result", e2)