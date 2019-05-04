from typing import List, Any, Union
from .lexer import Token


class AST:
    """Abstract Syntax Tree """
    def tree_repr(self) -> List[Any]:
        raise NotImplementedError

    def __str__(self) -> str:
        return str(self.tree_repr())

    def __repr__(self) -> str:
        return self.__str__()


class TokenBasedAST(AST):
    def __init__(self, token: Token) -> None:
        self.token = token
        self.value = token.value

    def tree_repr(self):
        return self.token.tree_repr()


class Var(TokenBasedAST):
    pass


class Num(TokenBasedAST):
    pass


class Bool(TokenBasedAST):
    pass


class String(TokenBasedAST):
    pass


ASTValueType = Union[String, Bool, Num]


class Constraint(AST):
    def __init__(self, var: Var, rel_op: Token, value: ASTValueType):
        self.var = var
        self.rel_op = rel_op
        self.value = value

    def tree_repr(self) -> List[Any]:
        return [
            self.var.tree_repr(),
            self.rel_op.tree_repr(),
            self.value.tree_repr(),
        ]


class BinOp(AST):
    def __init__(self, left: AST, op: Token, right: AST) -> None:
        self.left = left
        self.op = op
        self.right = right

    def tree_repr(self) -> List[Any]:
        return [
            self.left.tree_repr(),
            self.op.tree_repr(),
            self.right.tree_repr(),
        ]


class NoOp(AST):
    def tree_repr(self) -> List[Any]:
        return ['noop']
