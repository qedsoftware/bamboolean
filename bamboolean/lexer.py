import re
from functools import reduce
from collections import OrderedDict
from typing import NoReturn, Optional, Dict, Tuple, Union, Callable

from .exceptions import BambooleanLexerError
from . import tokens as tok


ValueType = Optional[Union[str, bool, int, float]]


class Token:
    def __init__(self, type: str, value: ValueType) -> None:
        self.type: str = type
        self.value: ValueType = value

    def __str__(self) -> str:
        return 'Token({type}, {value})'.format(
            type=self.type,
            value=repr(self.value))

    def stringify(self):
        return str(self.value).lower()

    def __repr__(self) -> str:
        return self.__str__()

    def tree_repr(self) -> Tuple[str, ValueType]:
        return self.type, self.value


RESERVED_KEYWORDS: Dict[str, Token] = {
    'AND': Token(tok.AND, 'AND'),
    'OR': Token(tok.OR, 'OR'),
    'NOT': Token(tok.NOT, 'NOT'),
    'TRUE': Token(tok.BOOL, True),
    'FALSE': Token(tok.BOOL, False),
}


class Lexer:
    def __init__(self, text: str) -> None:
        self.text = text
        self.position = 0
        self.current_char = self.text[self.position] if self.text else None

    def error(self) -> NoReturn:
        raise BambooleanLexerError(
            ("Error tokenizing input on character: "
             "{} and position: {}.\nExpr: {}".format(
                 self.current_char, self.position, self.text))
        )

    def _is_eof(self, pos: int) -> bool:
        return pos > len(self.text) - 1

    def next(self) -> None:
        """
        Set pointer to next character
        """
        self.position += 1
        is_eof = self._is_eof(self.position)
        self.current_char = self.text[self.position] if not is_eof else None

    def peek(self) -> Optional[str]:
        """
        Check what next char will be without advancing position
        """
        peek_pos = self.position + 1
        return self.text[peek_pos] if not self._is_eof(peek_pos) else None

    def id(self) -> Token:
        """
        Handle identifiers and reserved keywords
        """
        result = ''
        while self.current_char is not None and \
                re.match(r'[\w/]', self.current_char):
            result += self.current_char
            self.next()
        result = result.upper()
        token = RESERVED_KEYWORDS.get(result, Token(tok.ID, result))
        return token

    def skip_whitespace(self) -> None:
        while self.current_char is not None and self.current_char.isspace():
            self.next()

    @staticmethod
    def _is_quotation_mark(char: str) -> bool:
        return char == "'" or char == '"'

    def string(self) -> Token:
        self.next()  # skip opening quotation mark
        result = ''
        while self.current_char is not None and \
                not self._is_quotation_mark(self.current_char):
            result += self.current_char
            self.next()
        self.next()  # omit closing quote
        return Token(tok.STRING, result)

    def number(self) -> Token:
        result = str(self._integer())
        if self.current_char == '.':
            self.next()
            result += '.' + str(self._integer())
            return Token(tok.FLOAT, float(result))
        else:
            return Token(tok.INTEGER, int(result))

    def _integer(self) -> int:
        result = ''
        while self.current_char is not None and \
                self.current_char.isdigit():
            result += self.current_char
            self.next()
        return int(result)

    def skip_n_chars(self, n: int) -> None:
        for i in range(n):
            self.next()

    def is_token_equal(self, expected: str) -> bool:
        return expected == reduce(
            lambda actual, _: actual + str(self.peek()),
            range(len(expected)-1),
            str(self.current_char),
        )

    def get_next_token(self) -> Token:
        """
        Lexical analyzer (tokenizer). Breaks sentence apart into tokens
        """
        regex_map: Dict[str, Callable[[], Token]] = OrderedDict((
            (r'("|\')', self.string),
            (r'[_a-zA-Z]', self.id),
            (r'\d', self.number),
        ))

        tokens_map: Dict[str, Token] = OrderedDict((
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
