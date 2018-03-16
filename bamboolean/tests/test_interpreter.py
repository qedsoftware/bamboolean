import unittest
from collections import OrderedDict

from bamboolean.factories import interpret
from . import fixtures


class InterpreterTestCase(unittest.TestCase):
    def test_interpreter__basic(self):
        text = 'x > 42'
        self.assertTrue(interpret(text, {'x': 50}))
        self.assertFalse(interpret(text, {'x': 10}))

    def assertResults(self, expression, sym_tab, results):
        self.assertEqual(
            list(map((lambda args: interpret(
                expression,
                {symbol: args[i] for i, symbol in enumerate(sym_tab.keys())})
            ), zip(*tuple(sym_tab.values())))),
            results,
        )

    def test_interpreter(self):
        sym_tab = OrderedDict([
            ('x', [100, 90, 43, 42]),
            ('y', [False, True, False, False]),
            ('z', ['no', 'yes__typo', 'no', 'yes']),
        ])
        results = [True, False, True, True]
        self.assertResults(fixtures.simple_example, sym_tab, results)

    def test_parentheses(self):
        sym_tab = OrderedDict([
            ('x', [100, 10, 24, 10, 10]),
            ('y', ['yes', 'no', 'unknown', 'unknown', 'yes']),
        ])
        results = [True, True, True, False, False]
        self.assertResults(fixtures.parentheses, sym_tab, results)

    def test_operators_precedence(self):
        sym_tab = {
            'x': 1,
            'y': 'not eligible',
        }
        self.assertTrue(interpret(fixtures.operators_precedence, sym_tab))
