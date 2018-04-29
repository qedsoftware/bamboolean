import unittest

from bamboolean.lexer import Lexer
from bamboolean.exceptions import BambooleanLexerError
from bamboolean import tokens as tok
from .fixtures import simple_example


class LexerTestCase(unittest.TestCase):
    def test_tokens(self):
        records = (
            ('', tok.EOF, None),
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
            ('group/variable_name', tok.ID, 'GROUP/VARIABLE_NAME'),
            ("'text'", tok.STRING, 'text'),
            ('"text"', tok.STRING, 'text'),
            ('"it_is_still_string"', tok.STRING, 'it_is_still_string'),
            ('"this/also/works"', tok.STRING, 'this/also/works'),
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
        tokens = [token]

        while token.type != tok.EOF:
            token = lexer.get_next_token()
            tokens.append(token)

        self.assertEqual(list(map(lambda t: t.type, tokens)), [
            tok.ID, tok.GT, tok.INTEGER, tok.AND,
            tok.ID, tok.NE, tok.BOOL, tok.OR,
            tok.ID, tok.EQ, tok.STRING, tok.EOF,
        ])

    def test_lexer_raises_on_invalid_token(self):
        lexer = Lexer('@>>')
        with self.assertRaises(BambooleanLexerError):
            lexer.get_next_token()
