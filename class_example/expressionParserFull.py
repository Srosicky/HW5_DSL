# Need to install lark via pip
# pip install lark
# Note for me this puts it into the homebrew install of python,
#  so I need to run with the following rather than python3:
# /opt/homebrew/bin/python3.10 expressionParser.py
# otherwise it would just be: python expressionParser.py

# This is the multi statment, with assignment version
# meaning it has to have an environment for variables in evaulator
# and also uses the full grammar file with multi-line, assignment, variables included

# I removed the evaluator that runs directly through the parseTree
# as I really want to just turn the parseTree into an AST
# and write the evaluator on that

# This was modified from the version where the AST nodes are dataclasses rather than tuples

text = """
a = 10 + 2 * (3 - 4);
b = 1 + 2;
a + b;
"""

from lark import Lark
import os

current_dir = f'{os.getcwd()}/class_example/'
grammar_file = 'expressionGrammarFull.lark'

# Use LALR rather than Earley
# LALR works best with left recursive grammars
parser = Lark.open(current_dir + grammar_file, parser="lalr")
parseTree = parser.parse(text)
print(parseTree)
print(parseTree.pretty())
# The tree is a parse tree not an AST


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
class VarNode(Node):
    name: str

@dataclass
class AssignNode(Node):
    name: VarNode
    expr: Node

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
    
    def NAME(self, n):
        return VarNode(str(n))

    def start(self, children):
        return children[0]
       
    def statements(self, children):
        # Flatten the recursive list into a single Python list
        flat_list = []
        for child in children:
            if isinstance(child, list):
                flat_list.extend(child)
            elif isinstance(child, Node):
                flat_list.append(child)
        return flat_list

    def statement(self, children):
        return children[0]

    def assignment(self, children):
        # children[0] is the NAME, children[1] is the expr
        # the "=" was filtered out in the parser
        return AssignNode(children[0], children[1])
    
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
from typing import Dict, List

# Specific dictionary that binds strings to integers only
env: Dict[str, int] = {}

def evalAST(node: Node):

    if isinstance(node, ValNode):
        return node.value
    
    elif isinstance(node, VarNode):
        if node.name not in env:
            raise NameError(f"Undefined variable: {node.name}")
        return env[node.name]
    
    elif isinstance(node, AssignNode):
        # Evaluate the expression and save it to the environment
        value = evalAST(node.expr)
        # We need .name.name since the first one is to get the ValNode
        # and the second is to get the name of the value node
        # Note we don't ant to eval the ValNode as that will just give us a value back
        env[node.name.name] = value
        return value
    
    elif isinstance(node, AddNode):
        return evalAST(node.left) + evalAST(node.right)
    
    elif isinstance(node, SubNode):
        return evalAST(node.left) - evalAST(node.right)
    
    elif isinstance(node, MultNode):
        return evalAST(node.left) * evalAST(node.right)
    
    elif isinstance(node, DivNode):
        return evalAST(node.left) // evalAST(node.right)
    
    raise ValueError(f"Unknown node type: {type(node)}")

    

def evalProgram(nodes: List[Node]):
    last_result = 0
    for node in nodes:
        last_result = evalAST(node)
    return last_result


e2 = evalProgram(ast)
print("AST Evaluator Result", e2)