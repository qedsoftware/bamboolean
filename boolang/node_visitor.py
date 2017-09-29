from .exceptions import NoSuchVisitorException


class NodeVisitor(object):
    """Node visitor pattern implementation.

    Walk by each node in structure and invoke function coresponding to
    class name
    Example:
        class name: Node
        method: visit_Node()
    """
    def visit(self, node):
        method_name = 'visit_' + type(node).__name__
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):
        raise NoSuchVisitorException(
            'No visit_{} method'.format(type(node).__name__))
