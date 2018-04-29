# Types
STRING = 'STRING'
BOOL = 'BOOL'
INTEGER = 'INTEGER'
FLOAT = 'FLOAT'
ID = 'ID'

LPAREN, RPAREN, = ('(', ')')

# Operators
AND, OR = ('AND', 'OR')
NE, EQ, LT, LTE, GT, GTE = ('NE', 'EQ', 'LT', 'LTE', 'GT', 'GTE')

EOF = 'EOF'


def is_rel_op(op):
    return op in (NE, EQ, LT, LTE, GT, GTE)


def is_value(tok_type):
    return tok_type in (STRING, BOOL, INTEGER, FLOAT)
