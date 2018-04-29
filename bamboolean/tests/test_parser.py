import unittest

from bamboolean import tokens as tok
from bamboolean.exceptions import BambooleanParserError
from bamboolean.factories import ParserFactory
from . import fixtures


class ParserTestCase(unittest.TestCase):
    def test_parser(self):
        parser = ParserFactory(fixtures.simple_example)
        abstract_tree = parser.parse()
        self.assertEqual(abstract_tree.tree_repr(), [
            [
             [(tok.ID, 'X'), (tok.GT, '>'), (tok.INTEGER, 42)],
             (tok.AND, 'AND'),
             [(tok.ID, 'Y'), (tok.NE, '!='), (tok.BOOL, True)]
            ],
            (tok.OR, 'OR'),
            [(tok.ID, 'Z'), (tok.EQ, '=='), (tok.STRING, 'yes')]
        ])

    def test_parsing_parentheses(self):
        parser = ParserFactory(fixtures.parentheses)
        abstract_tree = parser.parse()
        self.assertEqual(abstract_tree.tree_repr(), [
            [
             [(tok.ID, 'X'), (tok.LTE, '<='), (tok.INTEGER, 42)],
             (tok.OR, 'OR'),
             [(tok.ID, 'Y'), (tok.EQ, '=='), (tok.STRING, 'yes')],
            ],
            (tok.AND, 'AND'),
            [
             [(tok.ID, 'Y'), (tok.EQ, '=='), (tok.STRING, 'no')],
             (tok.OR, 'OR'),
             [(tok.ID, 'X'), (tok.GTE, '>='), (tok.INTEGER, 17)]
            ],
        ])

    def test_operators_precedence(self):
        parser = ParserFactory(fixtures.operators_precedence)
        abstract_tree = parser.parse()
        self.assertEqual(abstract_tree.tree_repr(), [
            [(tok.ID, 'X'), (tok.LT, '<'), (tok.FLOAT, 5.15)],
            (tok.OR, 'OR'),
            [
             [(tok.ID, 'X'), (tok.GT, '>'), (tok.INTEGER, 10)],
             (tok.AND, 'AND'),
             [(tok.ID, 'Y'), (tok.EQ, '=='), (tok.STRING, 'eligible')],
            ],
        ])

    def test_implicit_boolean_cast(self):
        parser = ParserFactory(fixtures.implicit_boolean_cast)
        abstract_tree = parser.parse()
        self.assertEqual(abstract_tree.tree_repr(), [
            (tok.ID, 'Z'), (tok.OR, 'OR'),
            [(tok.ID, 'X'), (tok.AND, 'AND'), (tok.ID, 'Y')],
        ])

    def test_constant_statements(self):
        parser = ParserFactory(fixtures.constant_statements)
        abstract_tree = parser.parse()
        self.assertEqual(abstract_tree.tree_repr(), [
            [(tok.INTEGER, 444), (tok.AND, 'AND'), (tok.BOOL, True)],
            (tok.OR, 'OR'), (tok.STRING, 'yes'),
        ])

    def test_parser_raises_on_invalid_ast(self):
        parser = ParserFactory("x >>= f")
        with self.assertRaises(BambooleanParserError):
            parser.parse()

    def test_empty_expression(self):
        parser = ParserFactory('')
        abstract_tree = parser.parse()
        self.assertEqual(['noop'], abstract_tree.tree_repr())
