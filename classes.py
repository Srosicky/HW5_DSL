from dataclasses import dataclass
from typing import List
import dudraw
from lark import Transformer


# AST class
@dataclass
class Node:
    pass

@dataclass
class valNode(Node):
    number: float

@dataclass
class colorNode(Node):
    name: str

@dataclass
class forwardNode(Node):
    distance: float

@dataclass
class rotateNode(Node):
    angle: float

@dataclass
class penUpNode(Node):
    pass

@dataclass
class penDownNode(Node):
    pass

@dataclass
class repeatNode(Node):
    numRepeats: int
    bodyCmd: List[Node]


# Transformer class
class DrawingTransformer(Transformer):

    def start(self, children):
        return children[0]

    def statements(self, children):
        flat_list = []
        for child in children:
            if isinstance(child, list):
                flat_list.extend(child)
            else:
                flat_list.append(child)
        return flat_list

    def command(self, children):
        return children[0]

    def forward_cmd(self, children):
        return forwardNode(float(children[0]))

    def rotate_cmd(self, children):
        return rotateNode(float(children[0]))

    def penup_cmd(self, children):
        return penUpNode()

    def pendown_cmd(self, children):
        return penDownNode()

    def color_cmd(self, children):
        return colorNode(str(children[0]))

    def repeat_cmd(self, children):
        return repeatNode(int(children[0]), children[1])


# Pen Class
class DrawingPen:
    def __init__(self):
        self.color = "black"
        self.direction = 0.0
        self.x = 0.5
        self.y = 0.5
        self.is_down = False

    def move_forward(self, distance):
        pass  # TODO: implement with dudraw

    def rotate(self, degrees):
        pass  # TODO: implement with dudraw

    def pen_up(self):
        self.is_down = False

    def pen_down(self):
        self.is_down = True

    def change_color(self, color):
        self.color = color
        # TODO: dudraw.set_pen_color(...)