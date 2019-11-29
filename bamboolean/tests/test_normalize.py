import unittest

from bamboolean.factories import normalize


class NormalizeExpr(unittest.TestCase):
    def test_normalize_should_not_change_normalized_terms(self):
        self.assertEqual(normalize('false'), 'false')

    def test_normalize_negation(self):
        self.assertEqual(normalize('not x'), 'not x')
        self.assertEqual(normalize('not not x'), 'x')
        self.assertEqual(normalize('not not not x'), 'not x')

    def test_normalize_binop(self):
        self.assertEqual(normalize('not (x and not y)'), '(not x or y)')
        self.assertEqual(normalize('x or not not y'), '(x or y)')

    def test_normalize_empty(self):
        self.assertEqual(normalize(''), '')

    def test_normalize_bool(self):
        self.assertEqual(normalize('not false'), 'true')

    def test_normalize_relop(self):
        self.assertEqual(normalize('not (x >= 42)'), 'x < 42')
        self.assertEqual(normalize('not (x > 42)'), 'x <= 42')
        self.assertEqual(
            normalize('not (x > 42 and y)'), '(x <= 42 or not y)')
