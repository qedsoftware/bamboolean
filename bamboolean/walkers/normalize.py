from bamboolean.node_visitor import NodeVisitor
from bamboolean.ast import AST, Constraint, BinOp, UnaryOp, Bool
from bamboolean import tokens as tok


class NegateExpr(NodeVisitor):
    def __init__(self, tree: AST) -> None:
        self.tree = tree

    def demorgan(self) -> AST:
        """Negate expression just as De Morgan would do it."""
        return self.visit(self.tree)

    def visit_Constraint(self, node: Constraint) -> Constraint:
        new_op = tok.complementary_token[node.rel_op]
        return Constraint(node.var, new_op, node.value)

    def visit_BinOp(self, node: BinOp) -> BinOp:
        new_op = tok.complementary_token[node.op]
        return BinOp(self.visit(node.left), new_op, self.visit(node.right))

    def visit_UnaryOp(self, node: UnaryOp) -> AST:
        if node.op.type == tok.NOT:
            return NormalizeExpr(node.right).normalize()
        return node

    def visit_Var(self, node: AST) -> UnaryOp:
        return UnaryOp(op=tok.Token(tok.NOT, tok.NOT), right=node)

    def visit_Bool(self, node: Bool) -> Bool:
        flipped_token = tok.Token(node.token.type, not node.value)
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
        if node.op.type == tok.NOT:
            return NegateExpr(node.right).demorgan()
        return node

    def visit_BinOp(self, node: BinOp) -> AST:
        return BinOp(self.visit(node.left), node.op, self.visit(node.right))

    def generic_visit(self, node: AST) -> AST:
        return node
