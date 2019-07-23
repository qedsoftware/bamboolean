from typing import Set
from .node_visitor import NodeVisitor
from .ast import AST, TokenBasedAST


class VarsExtractor(NodeVisitor):
    def __init__(self, tree: AST) -> None:
        self.tree = tree

    def extract(self) -> Set[str]:
        if not self.tree:
            return set()
        return self.visit(self.tree)

    def visit_Constraint(self, node) -> Set[str]:
        return self.visit(node.var)

    def visit_BinOp(self, node) -> Set[str]:
        return self.visit(node.left) | self.visit(node.right)

    def visit_Var(self, node: TokenBasedAST) -> Set[str]:
        return {str(node.value)}

    def generic_visit(self, node: TokenBasedAST) -> Set[str]:
        return set()
