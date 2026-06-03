from classes import (
    Node, forwardNode, rotateNode, colorNode,
    penUpNode, penDownNode, repeatNode, DrawingPen
)
from typing import List
import dudraw

def evaluate(node: Node, pen: DrawingPen):
    if isinstance(node, forwardNode):
        pen.move_forward(node.distance)
    elif isinstance(node, rotateNode):
        pen.rotate(node.angle)
    elif isinstance(node, colorNode):
        pen.change_color(node.name)
    elif isinstance(node, penUpNode):
        pen.pen_up()
    elif isinstance(node, penDownNode):
        pen.pen_down()
    elif isinstance(node, repeatNode):
        for _ in range(node.numRepeats):
            for cmd in node.bodyCmd:
                evaluate(cmd, pen)


def evaluate_program(nodes: List[Node], pen: DrawingPen):
    for node in nodes:
        evaluate(node, pen)


COLOR_MAP = {
    "white":      dudraw.WHITE,
    "black":      dudraw.BLACK,
    "red":        dudraw.RED,
    "green":      dudraw.GREEN,
    "blue":       dudraw.BLUE,
    "cyan":       dudraw.CYAN,
    "magenta":    dudraw.MAGENTA,
    "yellow":     dudraw.YELLOW,
    "orange":     dudraw.ORANGE,
    "violet":     dudraw.VIOLET,
    "pink":       dudraw.PINK,
    "gray":       dudraw.GRAY,
    "light_gray": dudraw.LIGHT_GRAY,
    "dark_red":   dudraw.DARK_RED,
    "dark_green": dudraw.DARK_GREEN,
    "dark_blue":  dudraw.DARK_BLUE,
}

def get_color(color_name: str):
    key = color_name.lower()
    if key not in COLOR_MAP:
        raise ValueError(f"Unknown color: '{color_name}'. Available: {list(COLOR_MAP.keys())}")
    return COLOR_MAP[key]