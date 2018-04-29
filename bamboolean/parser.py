from .exceptions import BambooleanParserError
from .lexer import Lexer
from . import ast
from . import tokens as tok


class Parser:
    def __init__(self, lexer):
        assert isinstance(lexer, Lexer)
        self.lexer = lexer
        self.current_token = self.lexer.get_next_token()

    def parse(self):
        node = self.compound_expr()
        if self.current_token.type != tok.EOF:
            self.error("EOF while parsing given text")
        return node

    def error(self, extra=''):
        raise BambooleanParserError(
            ('Invalid syntax on: token {type}, val {val}. '
             '{extra}.\nExpression: {expr}'
             ).format(type=self.current_token.type,
                      val=self.current_token.value,
                      extra=extra,
                      expr=self.lexer.text))

    def consume(self, token_type):
        """
        If token match with expected token,
        consume current and get next token
        """
        if self.current_token.type == token_type:
            self.current_token = self.lexer.get_next_token()
        else:
            self.error("Expected: {}".format(token_type))

    def compound_expr(self):
        """
        compound_expr : expr
                      | empty
        """
        if self.current_token.type == tok.EOF:
            return self.empty()
        return self.expr()

    def expr(self):
        """
        expr: simple_expr (OR simple_expr)*
        """
        return self._parse_bin_op(self.simple_expr, tok.OR)

    def simple_expr(self):
        """
        simple_expr: term (AND term)*
        """
        return self._parse_bin_op(self.term, tok.AND)

    def _parse_bin_op(self, node_func, token_type):
        node = node_func()

        while self.current_token.type == token_type:
            token = self.current_token
            self.consume(token_type)
            node = ast.BinOp(left=node, op=token, right=node_func())

        return node

    def term(self):
        """
        term : statement
             | LPAREN expr RPAREN
        """
        if self.current_token.type == tok.LPAREN:
            self.consume(tok.LPAREN)
            node = self.expr()
            self.consume(tok.RPAREN)
            return node
        return self.statement()

    def statement(self):
        """
        statement : value
                  | constraint
        """
        if tok.is_value(self.current_token.type):
            return self.value()
        return self.constraint()

    def constraint(self):
        """
        constraint : variable (relational_operator value)?
        """
        var = self.variable()
        if tok.is_rel_op(self.current_token.type):
            rel_op = self.relational_op()
            val = self.value()
            return ast.Constraint(var, rel_op, val)
        return var

    def variable(self):
        """
        variable : ID
        """
        node = ast.Var(self.current_token)
        self.consume(tok.ID)
        return node

    def relational_op(self):
        """
        relational_operator : ( EQ | NE | LT | LTE | GT | GTE )
        """
        token = self.current_token
        if tok.is_rel_op(token.type):
            self.consume(token.type)
            return token
        self.error("Invalid relational operator")

    def value(self):
        """
        value : INTEGER
              | FLOAT
              | STRING
              | BOOL
        """
        token = self.current_token
        ast_mapping = {
            'INTEGER': ast.Num,
            'FLOAT': ast.Num,
            'STRING': ast.String,
            'BOOL': ast.Bool,
        }
        try:
            ast_class = ast_mapping[token.type]
        except KeyError:
            self.error("Invalid constraint value")
        else:
            self.consume(token.type)
            return ast_class(token)

    def empty(self):
        return ast.NoOp()
