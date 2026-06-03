from classes import (
    Node, forwardNode, rotateNode, colorNode,
    penUpNode, penDownNode, repeatNode, DrawingPen
)
from typing import List


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