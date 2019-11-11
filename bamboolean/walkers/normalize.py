from typing import TypeVar, Dict
from bamboolean.node_visitor import NodeVisitor
from bamboolean.ast import AST, Constraint, BinOp, UnaryOp, Bool
from bamboolean.lexer import Token
from bamboolean.tokens import NOT


T1 = TypeVar('T1')
T2 = TypeVar('T2')


def flip_dict(d: Dict[T1, T2]) -> Dict[T2, T1]:
    return {v: k for k, v in d.items()}


def complementary_op(op):
    flip_op = {
        ('EQ', '=='): ('NE', '!='),
        ('LT', '<'): ('GTE', '>='),
        ('LTE', '<='): ('GT', '>'),
        ('OR', 'OR'): ('AND', 'AND')
    }
    return {**flip_op, **flip_dict(flip_op)}[op]


class NegateExpr(NodeVisitor):
    def __init__(self, tree: AST) -> None:
        self.tree = tree

    def demorgan(self) -> AST:
        """Negate expression just as De Morgan would do it."""
        return self.visit(self.tree)

    def visit_Constraint(self, node: Constraint) -> Constraint:
        current_op = (node.rel_op.type, node.rel_op.value)
        new_op = Token(*complementary_op(current_op))
        return Constraint(node.var, new_op, node.value)

    def visit_BinOp(self, node: BinOp) -> BinOp:
        op_type, op_value = complementary_op((node.op.type, node.op.value))
        op = Token(op_type, op_value)
        return BinOp(self.visit(node.left), op, self.visit(node.right))

    def visit_UnaryOp(self, node: UnaryOp) -> AST:
        if node.op.type == NOT:
            return NormalizeExpr(node.right).normalize()
        return node

    def visit_Var(self, node: AST) -> UnaryOp:
        return UnaryOp(op=Token(NOT, NOT), right=node)

    def visit_Bool(self, node: Bool) -> Bool:
        flipped_token = Token(node.token.type, not node.value)
        return Bool(token=flipped_token)

    def generic_visit(self, node: AST) -> AST:
        return node


class NormalizeExpr(NodeVisitor):
    def __init__(self, tree: AST) -> None:
        self.tree = tree

    def normalize(self) -> AST:
        """Convert the expression to the normal form"""
        return self.visit(self.tree)

    def visit_UnaryOp(self, node: UnaryOp) -> AST:
        if node.op.type == NOT:
            return NegateExpr(node.right).demorgan()
        return node

    def visit_BinOp(self, node: BinOp) -> AST:
        return BinOp(self.visit(node.left), node.op, self.visit(node.right))

    def generic_visit(self, node: AST) -> AST:
        return node
