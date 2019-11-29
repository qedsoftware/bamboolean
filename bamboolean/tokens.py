from collections import OrderedDict
from typing import Optional, Dict, Union, Tuple, TypeVar

T1 = TypeVar('T1')
T2 = TypeVar('T2')


# Types
STRING = 'STRING'
BOOL = 'BOOL'
INTEGER = 'INTEGER'
FLOAT = 'FLOAT'
ID = 'ID'

LPAREN, RPAREN, = ('(', ')')

# Operators
AND, OR, NOT = ('AND', 'OR', 'NOT')
NE, EQ, LT, LTE, GT, GTE = ('NE', 'EQ', 'LT', 'LTE', 'GT', 'GTE')

EOF = 'EOF'

ValueType = Optional[Union[str, bool, int, float]]


class Token:
    def __init__(self, type: str, value: ValueType) -> None:
        self.type: str = type
        self.value: ValueType = value

    def __str__(self) -> str:
        return 'Token({type}, {value})'.format(
            type=self.type,
            value=repr(self.value))

    def __hash__(self) -> int:
        return hash((self.type, self.value))

    def __eq__(self, other) -> bool:
        return self.__hash__() == other.__hash__()

    def stringify(self) -> str:
        return str(self.value).lower()

    def __repr__(self) -> str:
        return self.__str__()

    def tree_repr(self) -> Tuple[str, ValueType]:
        return self.type, self.value


def flip_dict(d: Dict[T1, T2]) -> Dict[T2, T1]:
    return {v: k for k, v in d.items()}


def is_unary_op(op: str) -> bool:
    return op in (NOT,)


def is_rel_op(op: str) -> bool:
    return op in (NE, EQ, LT, LTE, GT, GTE)


def is_value(tok_type: str) -> bool:
    return tok_type in (STRING, BOOL, INTEGER, FLOAT)


RESERVED_KEYWORDS: Dict[str, Token] = {
    'AND': Token(AND, 'AND'),
    'OR': Token(OR, 'OR'),
    'NOT': Token(NOT, 'NOT'),
    'TRUE': Token(BOOL, True),
    'FALSE': Token(BOOL, False),
}

abstract_syntax: Dict[str, str] = OrderedDict((
    ('==', EQ),
    ('!=', NE),
    ('<=', LTE),
    ('>=', GTE),
    ('>', GT),
    ('<', LT),
    ('(', LPAREN),
    (')', RPAREN),
    ('OR', OR),
    ('AND', AND),
))
concrete_syntax = flip_dict(abstract_syntax)

tokens_map: Dict[str, Token] = OrderedDict((
    (concrete, Token(abstract, concrete))
    for concrete, abstract in abstract_syntax.items()
))
abstract_tokens_map: Dict[str, Token] = OrderedDict((
    (abstract, Token(abstract, concrete))
    for concrete, abstract in abstract_syntax.items()
))

flip_op: Dict[str, str] = {
    EQ: NE,
    LT: GTE,
    LTE: GT,
    OR: AND,
}
complementary_op: Dict[str, str] = {**flip_op, **flip_dict(flip_op)}

complementary_token: Dict[Token, Token] = {
    abstract_tokens_map[op2]: abstract_tokens_map[op1]
    for op1, op2 in complementary_op.items()
}
