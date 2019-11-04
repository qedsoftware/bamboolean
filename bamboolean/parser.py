from typing import NoReturn, Dict, Type, Union, Callable
from .exceptions import BambooleanParserError
from .lexer import Lexer, Token
from . import ast
from . import tokens as tok


ParseNodeT = Callable[[], ast.AST]


class Parser:
    def __init__(self, lexer: Lexer) -> None:
        self.lexer = lexer
        self.current_token = self.lexer.get_next_token()

    def parse(self) -> ast.AST:
        node = self.compound_expr()
        if self.current_token.type != tok.EOF:
            self.error("EOF while parsing given text")
        return node

    def error(self, extra='') -> NoReturn:
        raise BambooleanParserError(
            ('Invalid syntax on: token {type}, val {val}. '
             '{extra}.\nExpression: {expr}'
             ).format(type=self.current_token.type,
                      val=self.current_token.value,
                      extra=extra,
                      expr=self.lexer.text))

    def consume(self, token_type) -> None:
        """
        If token match with expected token,
        consume current and get next token
        """
        if self.current_token.type == token_type:
            self.current_token = self.lexer.get_next_token()
        else:
            self.error("Expected: {}".format(token_type))

    def compound_expr(self) -> ast.AST:
        """
        compound_expr : expr
                      | empty
        """
        if self.current_token.type == tok.EOF:
            return self.empty()
        return self.expr()

    def expr(self) -> ast.AST:
        """
        expr: simple_expr (OR simple_expr)*
        """
        return self._parse_bin_op(self.simple_expr, tok.OR)

    def simple_expr(self) -> ast.AST:
        """
        simple_expr: term (AND term)*
        """
        return self._parse_bin_op(self.term, tok.AND)

    def _parse_bin_op(self, node_func: ParseNodeT, token_type) -> ast.AST:
        node = node_func()

        while self.current_token.type == token_type:
            token = self.current_token
            self.consume(token_type)
            node = ast.BinOp(left=node, op=token, right=node_func())

        return node

    def _parse_unary_op(self, node_func: ParseNodeT) -> ast.AST:
        token = self.current_token
        self.consume(token.type)
        return ast.UnaryOp(op=token, right=node_func())

    def term(self) -> ast.AST:
        """
        term : statement
             | LPAREN expr RPAREN
             | NOT term
        """
        if self.current_token.type == tok.LPAREN:
            self.consume(tok.LPAREN)
            node = self.expr()
            self.consume(tok.RPAREN)
            return node
        if tok.is_unary_op(self.current_token.type):
            return self._parse_unary_op(self.term)
        return self.statement()

    def statement(self) -> Union[ast.ASTValueType, ast.Var, ast.Constraint]:
        """
        statement : value
                  | constraint
        """
        if tok.is_value(self.current_token.type):
            return self.value()
        return self.constraint()

    def constraint(self) -> Union[ast.Var, ast.Constraint]:
        """
        constraint : variable (relational_operator value)?
        """
        var = self.variable()
        if tok.is_rel_op(self.current_token.type):
            rel_op = self.relational_op()
            val = self.value()
            return ast.Constraint(var, rel_op, val)
        return var

    def variable(self) -> ast.Var:
        """
        variable : ID
        """
        node = ast.Var(self.current_token)
        self.consume(tok.ID)
        return node

    def relational_op(self) -> Token:
        """
        relational_operator : ( EQ | NE | LT | LTE | GT | GTE )
        """
        token = self.current_token
        if tok.is_rel_op(token.type):
            self.consume(token.type)
        else:
            self.error("Invalid relational operator")
        return token

    def value(self) -> ast.ASTValueType:
        """
        value : INTEGER
              | FLOAT
              | STRING
              | BOOL
        """
        token = self.current_token
        ast_mapping: Dict[str, Type[ast.ASTValueType]] = {
            'INTEGER': ast.Num,
            'FLOAT': ast.Num,
            'STRING': ast.String,
            'BOOL': ast.Bool,
        }
        try:
            ast_class = ast_mapping[token.type]
        except KeyError:
            self.error("Invalid constraint value")
        self.consume(token.type)
        return ast_class(token)

    def empty(self) -> ast.NoOp:
        return ast.NoOp()
