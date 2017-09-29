
class AST:
    """Abstract Syntax Tree """
    def tree_repr(self):
        raise NotImplementedError

    def __str__(self):
        return str(self.tree_repr())

    def __repr__(self):
        return self.__str__()


class TokenBasedAST(AST):
    def __init__(self, token):
        self.token = token
        self.value = token.value

    def tree_repr(self):
        return self.token.tree_repr()


class Constraint(AST):
    def __init__(self, var, rel_op, value):
        self.var = var
        self.rel_op = rel_op
        self.value = value

    def tree_repr(self):
        return [
            self.var.tree_repr(),
            self.rel_op.tree_repr(),
            self.value.tree_repr(),
        ]


class BinOp(AST):
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right

    def tree_repr(self):
        return [
            self.left.tree_repr(),
            self.op.tree_repr(),
            self.right.tree_repr(),
        ]


class Var(TokenBasedAST):
    pass


class Num(TokenBasedAST):
    pass


class Bool(TokenBasedAST):
    pass


class String(TokenBasedAST):
    pass
