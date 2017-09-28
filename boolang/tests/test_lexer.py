import unittest

from boolang.lexer import Lexer
from boolang import tokens as tok
from .fixtures import simple_example


class LexerTestCase(unittest.TestCase):
    def test_tokens(self):
        records = (
            ('42', tok.INTEGER, 42),
            ('3.14', tok.FLOAT, 3.14),
            ('true', tok.BOOL, True),
            ('false', tok.BOOL, False),
            ('AND', tok.AND, 'AND'),
            ('OR', tok.OR, 'OR'),
            ('(', tok.LPAREN, '('),
            (')', tok.RPAREN, ')'),
            ('var', tok.ID, 'VAR'),
            ('another_var_1', tok.ID, 'ANOTHER_VAR_1'),
            ("'text'", tok.STRING, 'text'),
            ('"text"', tok.STRING, 'text'),
            ('>', tok.GT, '>'),
            ('<', tok.LT, '<'),
            ('<=', tok.LTE, '<='),
            ('>=', tok.GTE, '>='),
            ('==', tok.EQ, '=='),
            ('!=', tok.NE, '!='),
        )
        for text, tok_type, tok_val in records:
            lexer = Lexer(text)
            token = lexer.get_next_token()
            self.assertEqual(token.type, tok_type)
            self.assertEqual(token.value, tok_val)

    def test_lexer(self):
        lexer = Lexer(simple_example)
        token = lexer.get_next_token()
        tokens = []

        while token.type != tok.EOF:
            tokens.append(token)
            token = lexer.get_next_token()

        self.assertEqual(list(map(lambda t: t.type, tokens)), [
            tok.ID, tok.GT, tok.INTEGER, tok.AND,
            tok.ID, tok.NE, tok.BOOL, tok.OR,
            tok.ID, tok.EQ, tok.STRING,
        ])
