import operator as built_in_op

from . import tokens as tok
from .node_visitor import NodeVisitor


class Interpreter(NodeVisitor):
    def __init__(self, tree, symbol_table):
        self.tree = tree
        self.symbol_table = {k.upper(): v for k, v in symbol_table.items()}

    def interpret(self):
        if not self.tree:
            return False
        return self.visit(self.tree)

    def visit_BinOp(self, node):
        op_type = node.op.type

        if op_type == tok.AND:
            return self.visit(node.left) and self.visit(node.right)
        elif op_type == tok.OR:
            return self.visit(node.left) or self.visit(node.right)

    def visit_Constraint(self, node):
        var_value = self.visit(node.var)
        value = self.visit(node.value)
        return self._handle_rel_op(node.rel_op.type, var_value, value)

    def _handle_rel_op(self, op_type, val1, val2):
        mapping = {
            'NE': built_in_op.ne,
            'EQ': built_in_op.eq,
            'LT': built_in_op.lt,
            'LTE': built_in_op.le,
            'GT': built_in_op.gt,
            'GTE': built_in_op.ge,
        }
        op = mapping[op_type]
        return op(val1, val2)

    def visit_Var(self, node):
        var_name = node.value
        return self.symbol_table.get(var_name, '')

    def visit_Num(self, node):
        return node.value

    def visit_Bool(self, node):
        return node.value

    def visit_String(self, node):
        return node.value
