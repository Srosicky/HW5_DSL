import dudraw
from lark import Lark




text = "hello, I am sophie and I am doing this homework!"

parser = Lark.open("expressionGrammar.lark", parser="lalr")
parseTree = parser.parse(text)
print(parseTree)
print(parseTree.pretty())


