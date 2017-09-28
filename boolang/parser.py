from . import ast
from . import tokens as tok


class Parser:
    def __init__(self, lexer):
        self.lexer = lexer
        self.current_token = self.lexer.get_next_token()

    def parse(self):
        node = self.expr()
        if self.current_token.type != tok.EOF:
            self.error("EOF while parsing given text")
        return node

    def error(self, extra=''):
        raise SyntaxError(
            'Invalid syntax on: token {type}, val {val}. {extra}'.format(
                type=self.current_token.type,
                val=self.current_token.value,
                extra=extra))

    def consume(self, token_type):
        """
        If token match with expected token,
        consume current and get next token
        """
        if self.current_token.type == token_type:
            self.current_token = self.lexer.get_next_token()
        else:
            self.error("Expected: {}".format(token_type))

    def expr(self):
        """
        expr: simple_expr (OR simple_expr)*
        """
        node = self.simple_expr()

        while self.current_token.type == tok.OR:
            token = self.current_token
            self.consume(tok.OR)
            node = ast.BinOp(left=node, op=token, right=self.simple_expr())

        return node

    def simple_expr(self):
        """
        simple_expr: term (AND term)*
        """
        node = self.term()

        while self.current_token.type == tok.AND:
            token = self.current_token
            self.consume(tok.AND)
            node = ast.BinOp(left=node, op=token, right=self.term())

        return node

    def term(self):
        if self.current_token.type == tok.LPAREN:
            self.consume(tok.LPAREN)
            node = self.expr()
            self.consume(tok.RPAREN)
            return node
        else:
            var = self.variable()
            rel_op = self.relational_op()
            val = self.value()
            return ast.Constraint(var, rel_op, val)

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
        if token.type in (tok.EQ, tok.NE, tok.LT, tok.LTE, tok.GT, tok.GTE):
            self.consume(token.type)
            return token
        else:
            self.error("Invalid relational operator")

    def value(self):
        """
        value : INTEGER | FLOAT | STRING | BOOL
        """
        token = self.current_token

        if token.type in [tok.INTEGER, tok.FLOAT]:
            self.consume(token.type)
            return ast.Num(token)

        elif token.type == tok.STRING:
            self.consume(tok.STRING)
            return ast.String(token)

        elif token.type == tok.BOOL:
            self.consume(tok.BOOL)
            return ast.Bool(token)

        else:
            self.error("Invalid constraint value")
