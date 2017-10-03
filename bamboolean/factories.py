from .lexer import Lexer
from .parser import Parser
from .interpreter import Interpreter


def ParserFactory(text):
    lexer = Lexer(text)
    return Parser(lexer)


def InterpreterFactory(text, symbol_table):
    parser = ParserFactory(text)
    tree = parser.parse()
    return Interpreter(tree, symbol_table)
