import re
from functools import reduce
from collections import OrderedDict

from .exceptions import BambooleanLexerError
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
        return self.type, self.value


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
        raise BambooleanLexerError(
            """Error tokenizing input on character: {} and position: {}
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
        self.next()  # skip opening quotation mark
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

    def skip_n_chars(self, n):
        for i in range(n):
            self.next()

    def is_token_equal(self, expected):
        return expected == reduce(
            lambda actual, _: actual + str(self.peek()),
            range(len(expected)-1),
            self.current_char,
        )

    def get_next_token(self):
        """
        Lexical analyzer (tokenizer). Breaks sentence apart into tokens
        """
        regex_map = OrderedDict((
            (r'("|\')', self.string),
            (r'[_a-zA-Z]', self.id),
            (r'\d', self.number),
        ))

        tokens_map = OrderedDict((
            ('==', Token(tok.EQ, '==')),
            ('!=', Token(tok.NE, '!=')),
            ('<=', Token(tok.LTE, '<=')),
            ('>=', Token(tok.GTE, '>=')),
            ('>', Token(tok.GT, '>')),
            ('<', Token(tok.LT, '<')),
            ('(', Token(tok.LPAREN, '(')),
            (')', Token(tok.RPAREN, ')')),
        ))

        while self.current_char is not None:
            if self.current_char.isspace():
                self.skip_whitespace()
                continue

            for regex, func in regex_map.items():
                if re.match(regex, self.current_char):
                    return func()

            for expected_val, token in tokens_map.items():
                if self.is_token_equal(expected_val):
                    self.skip_n_chars(len(expected_val))
                    return token

            self.error()

        return Token(tok.EOF, None)
