from typing import Any
from .exceptions import NoSuchVisitorException


class NodeVisitor:
    """Node visitor pattern implementation.

    Walk by each node in structure and invoke function coresponding to
    class name
    Example:
        class name: Node
        method: visit_Node()
    """
    def visit(self, node) -> Any:
        method_name = 'visit_' + type(node).__name__
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node) -> Any:
        raise NoSuchVisitorException(
            'No visit_{} method'.format(type(node).__name__))
