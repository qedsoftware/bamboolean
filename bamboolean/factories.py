from .ast import AST
from .lexer import Lexer
from .parser import Parser
from .interpreter import Interpreter
from .walkers import VarsExtractor


def ParserFactory(text: str) -> Parser:
    lexer = Lexer(text)
    return Parser(lexer)


def InterpreterFactory(text: str, symbol_table: dict) -> Interpreter:
    parser = ParserFactory(text)
    tree = parser.parse()
    return Interpreter(tree, symbol_table)


def interpret(text: str, symbol_table: dict) -> bool:
    return InterpreterFactory(text, symbol_table).interpret()


def parse(text: str) -> AST:
    return ParserFactory(text).parse()


def extract(text: str):
    return VarsExtractor(parse(text)).extract()
