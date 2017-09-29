import re

from .exceptions import LexerError
from . import tokens as tok


class Token:
    def __init__(self, type, value):
        self.type = type
        self.value = value

    def __str__(self):
        return 'Token({type}, {value})'.format(
            type=self.type,
            value=repr(self.value))

    def __repr__(self):
        return self.__str__()

    def tree_repr(self):
        return (self.type, self.value)


RESERVED_KEYWORDS = {
    'AND': Token(tok.AND, 'AND'),
    'OR': Token(tok.OR, 'OR'),
    'TRUE': Token(tok.BOOL, True),
    'FALSE': Token(tok.BOOL, False),
}


class Lexer:
    def __init__(self, text):
        self.text = text
        self.position = 0
        self.current_char = self.text[self.position]

    def error(self):
        raise LexerError(
            """Error tokenizing input on character: {} and {} position
            """.format(self.current_char, self.position)
        )

    def _is_eof(self, pos):
        return pos > len(self.text) - 1

    def next(self):
        """
        Set pointer to next character
        """
        self.position += 1
        is_eof = self._is_eof(self.position)
        self.current_char = self.text[self.position] if not is_eof else None

    def peek(self):
        """
        Check what next char will be without advancing position
        """
        peek_pos = self.position + 1
        return self.text[peek_pos] if not self._is_eof(peek_pos) else None

    def id(self):
        """
        Handle identifiers and reserved keywords
        """
        result = ''
        while self.current_char is not None and \
                re.match('\w', self.current_char):
            result += self.current_char
            self.next()
        result = result.upper()
        token = RESERVED_KEYWORDS.get(result, Token(tok.ID, result))
        return token

    def skip_whitespace(self):
        while self.current_char is not None and self.current_char.isspace():
            self.next()

    @staticmethod
    def _is_quotation_mark(char):
        return char == "'" or char == '"'

    def string(self):
        result = ''
        while not self._is_quotation_mark(self.current_char):
            result += self.current_char
            self.next()
        self.next()  # omit closing quote
        return Token(tok.STRING, result)

    def number(self):
        result = str(self._integer())
        if self.current_char == '.':
            self.next()
            result += '.' + str(self._integer())
            return Token(tok.FLOAT, float(result))
        else:
            return Token(tok.INTEGER, int(result))

    def _integer(self):
        result = ''
        while self.current_char is not None and \
                self.current_char.isdigit():
            result += self.current_char
            self.next()
        return int(result)

    def get_next_token(self):
        """
        Lexical anaylzer (tokenizer). Breaks sentence apart into tokens
        """
        while self.current_char is not None:
            if self.current_char.isspace():
                self.skip_whitespace()
                continue

            if re.match('[_a-zA-Z]', self.current_char):
                return self.id()

            if self._is_quotation_mark(self.current_char):
                self.next()
                return self.string()

            if self.current_char.isdigit():
                return self.number()

            # Relational operators

            if self.current_char is '=' and self.peek() == '=':
                self.next()
                self.next()
                return Token(tok.EQ, '==')

            if self.current_char is '!' and self.peek() == '=':
                self.next()
                self.next()
                return Token(tok.NE, '!=')

            if self.current_char is '<':
                # LTE, LT
                self.next()
                if self.current_char is '=':
                    self.next()
                    return Token(tok.LTE, '<=')
                else:
                    return Token(tok.LT, '<')

            if self.current_char is '>':
                # GTE, GT
                self.next()
                if self.current_char is '=':
                    self.next()
                    return Token(tok.GTE, '>=')
                else:
                    return Token(tok.GT, '>')

            # Parentheses

            if self.current_char == '(':
                self.next()
                return Token(tok.LPAREN, '(')

            if self.current_char == ')':
                self.next()
                return Token(tok.RPAREN, ')')

            self.error()

        return Token(tok.EOF, None)
