from numbers import Number
from typing import Any, NoReturn
import operator as built_in_op

from . import tokens as tok
from .exceptions import BambooleanRuntimeError
from .ast import AST, TokenBasedAST
from .node_visitor import NodeVisitor


class Interpreter(NodeVisitor):
    def __init__(self, tree: AST, symbol_table: dict) -> None:
        self.tree = tree
        self.symbol_table = {k.upper(): v for k, v in symbol_table.items()}

    def interpret(self) -> bool:
        if not self.tree:
            return False
        return self.visit(self.tree)

    def error(self, extra='') -> NoReturn:
        raise BambooleanRuntimeError(
            "Runtime error occured. {extra}".format(extra=extra))

    def visit_BinOp(self, node) -> bool:
        op_type = node.op.type
        if op_type == tok.AND:
            return self.visit(node.left) and self.visit(node.right)
        elif op_type == tok.OR:
            return bool(self.visit(node.left) or self.visit(node.right))
        else:
            self.error("Could not evaluate binary operator")

    def visit_Constraint(self, node) -> bool:
        var_value = self.visit(node.var)
        value = self.visit(node.value)
        return self._handle_rel_op(node.rel_op.type, var_value, value)

    @staticmethod
    def _handle_rel_op(op_type: str, val1, val2) -> bool:
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

    def visit_Var(self, node: TokenBasedAST) -> Any:
        var_name = node.value
        return self.symbol_table.get(var_name, '')

    def visit_Num(self, node) -> Number:
        return node.value

    def visit_Bool(self, node) -> bool:
        return node.value

    def visit_String(self, node) -> str:
        return node.value

    def visit_NoOp(self, node) -> bool:
        return True  # no expression should evaluate to true
