import dudraw
from lark import Lark

#Based on the grammar in grammar.lark, 
#This should parse it and create and AST that can then be used to draw with

text = "repeat 30 (pendown forward 20 rotate 30 forward 10)"

parser = Lark.open("grammar.lark", parser="lalr")
parseTree = parser.parse(text)
print(parseTree)
print(parseTree.pretty())


#Now the python dataclasses

from dataclasses import dataclass

@dataclass
class Node:
    pass

@dataclass
class valNode:
    number : float

@dataclass
class colorNode:
    name : str

@dataclass
class forwardNode:
    distance: float

@dataclass
class rotateNode:
    angle: float

@dataclass
class repeatNode:
    numRepeats: int
    bodyCmd: list


##This is the transformer, which allows us to use our classes

from lark import Transformer

class ExpressionTransformer(Transformer):
    def forwardCommand(self, children):
        return forwardNode(float(children[0]))

    def rotateCommand(self, children):
        return rotateNode(float(children[0]))

    def repeatCommand(self, children):
        return repeatNode(int(children[0]), children[1])
    
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
    


###Now the drawing time:
#

class DrawingPen():
    def __init__(self):
        self.color = "BLACK"    # Instance attribute
        self.direction = 25.0

    def moveForward(self, distance):
        pass

    def rotate(self, degrees):
        pass

    def penup():
        pass

    def penDown():
        pass 

    def changeColor(self, Color):
        pass



#Evaluator function:
#Translates the AST to pen class calls:

def evaluate(node, pen):
    if isinstance(node, forwardNode):
        pen.move_forward(node.distance)

    elif isinstance(node, rotateNode):
        pen.rotate(node.angle)

    elif isinstance(node, colorNode):
        pen.ChangeColor(node.color)
    #repeat case, for the body text!
    elif isinstance(node, repeatNode):
        for i in range(node.numRepeats):
            for cmd in node.bodyCmd:
                evaluate(cmd, pen)