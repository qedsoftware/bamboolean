import unittest

from bamboolean.factories import interpret
from . import fixtures


class InterpreterTestCase(unittest.TestCase):
    def test_interpreter__basic(self):
        text = 'x > 42'
        self.assertTrue(interpret(text, {'x': 50}))
        self.assertFalse(interpret(text, {'x': 10}))

    def test_interpreter(self):
        sym_tab = {
            'x': [100, 90, 43, 42],
            'y': [False, True, False, False],
            'z': ['no', 'yes__typo', 'no', 'yes'],
            'results': [True, False, True, True],
        }
        self.assertEqual(
            list(map((lambda args: interpret(
                fixtures.simple_example,
                {'x': args[0], 'y': args[1], 'z': args[2]})
            ), zip(sym_tab['x'], sym_tab['y'], sym_tab['z']))),
            sym_tab['results'],
        )

    def test_parentheses(self):
        sym_tab = {
            'x': 100,
            'y': 'yes',
        }
        self.assertTrue(interpret(fixtures.parentheses, sym_tab))

    def test_operators_precedence(self):
        sym_tab = {
            'x': 1,
            'y': 'not eligible',
        }
        self.assertTrue(interpret(fixtures.operators_precedence, sym_tab))
