import unittest

from boolang import tokens as tok
from boolang.factories import ParserFactory
from .fixtures import simple_example


class ParserTestCase(unittest.TestCase):
    def test_parser(self):
        parser = ParserFactory(simple_example)
        abstract_tree = parser.parse()
        self.assertEqual(abstract_tree.tree_repr(), [
            [
             [(tok.ID, 'X'), (tok.GT, '>'), (tok.INTEGER, 10)],
             (tok.AND, 'AND'),
             [(tok.ID, 'Y'), (tok.NE, '!='), (tok.BOOL, True)]
            ],
            (tok.OR, 'OR'),
            [(tok.ID, 'Z'), (tok.EQ, '=='), (tok.STRING, 'none')]
        ])
