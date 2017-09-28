from .lexer import Lexer
from .parser import Parser


def ParserFactory(text):
    lexer = Lexer(text)
    return Parser(lexer)
