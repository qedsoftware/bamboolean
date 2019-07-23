import unittest

from bamboolean.factories import extract
from . import fixtures


class VarsExtractorTestCase(unittest.TestCase):
    def test_simple_example(self):
        self.assertCountEqual(
            extract(fixtures.simple_example), {'X', 'Y', 'Z'})

    def test_parentheses(self):
        self.assertCountEqual(extract(fixtures.parentheses), {'X', 'Y'})

    def test_operators_precedence(self):
        self.assertCountEqual(
            extract(fixtures.operators_precedence), {'X', 'Y'})

    def test_implicit_boolean_cast(self):
        self.assertCountEqual(
            extract(fixtures.implicit_boolean_cast), {'X', 'Y', 'Z'})

    def test_many_vars(self):
        variables = {f'VAR{i}' for i in range(30)}
        self.assertCountEqual(extract(' OR '.join(variables)), variables)
