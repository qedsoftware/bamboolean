import unittest

from bamboolean.factories import InterpreterFactory
from . import fixtures


def _interpret(text, symbol_table):
    return InterpreterFactory(text, symbol_table).interpret()


class InterpreterTestCase(unittest.TestCase):
    def test_interpreter__basic(self):
        text = 'x > 42'
        self.assertTrue(_interpret(text, {'x': 50}))
        self.assertFalse(_interpret(text, {'x': 10}))

    def test_interpreter(self):
        sym_tab = {
            'x': 100,
            'y': False,
            'z': 'yes',
        }
        self.assertTrue(_interpret(fixtures.simple_example, sym_tab))

    def test_parentheses(self):
        sym_tab = {
            'x': 100,
            'y': 'yes',
        }
        self.assertTrue(_interpret(fixtures.parentheses, sym_tab))

    def test_operators_precedence(self):
        sym_tab = {
            'x': 1,
            'y': 'not eligible',
        }
        self.assertTrue(_interpret(fixtures.operators_precedence, sym_tab))
