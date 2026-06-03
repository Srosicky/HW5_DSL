import dudraw
import math

from lark import Transformer
from dataclasses import dataclass
from typing import List


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
        self.color = dudraw.BLACK
        self.direction = 0.0
        self.x = 0.5
        self.y = 0.5
        self.is_down = False

    def move_forward(self, distance):
        # compute endpoint using current direction
        angle_rad = math.radians(self.direction)
        new_x = self.x + distance * math.cos(angle_rad)
        new_y = self.y + distance * math.sin(angle_rad)

        # only draw if the pen is already down...
        if self.is_down:
            dudraw.set_pen_color(self.color)
            dudraw.line(self.x, self.y, new_x, new_y)
        
        self.x = new_x
        self.y = new_y

    def rotate(self, degrees):
        self.direction = (self.direction + degrees) % 360

    def pen_up(self):
        self.is_down = False

    def pen_down(self):
        self.is_down = True

    def change_color(self, color_name: str):
        from helpers import get_color
        self.color = get_color(color_name)