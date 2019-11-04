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


def is_un_op(op: str) -> bool:
    return op in (NOT,)


def is_rel_op(op: str) -> bool:
    return op in (NE, EQ, LT, LTE, GT, GTE)


def is_value(tok_type: str) -> bool:
    return tok_type in (STRING, BOOL, INTEGER, FLOAT)
