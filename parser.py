from abc import ABC
from typing import List

from lexer import Lexer, Token
from utils import log_error


class ExprAST(ABC):
    pass


class ExprChangePtr(ExprAST):

    def __init__(self, offset):
        self.offset = offset

    def __repr__(self):
        if self.offset >= 0:
            sign = Token.INC_PTR.value
        else:
            sign = Token.DEC_PTR.value
        return str(self.offset) + sign

    def __eq__(self, other):
        if isinstance(self, other.__class__):
            return self.offset == other.offset
        return False


class ExprChangeValue(ExprAST):

    def __init__(self, offset=0, value=1):
        self.value = value
        self.offset = offset

    def __repr__(self):
        if self.value >= 0:
            sign = '+'
        else:
            sign = '-'
        return f"[{self.offset}]{sign}={abs(self.value)}"

    def __eq__(self, other):
        if isinstance(self, other.__class__):
            return self.offset == other.offset and \
                self.value == other.value
        return False


class ExprBlock(ExprAST):
    expressions = List[ExprAST]

    def __init__(self, expressions: List[ExprAST]):
        self.expressions = expressions

    def __repr__(self):
        return ' '.join([str(expr) for expr in self.expressions])

    def __eq__(self, other):
        if isinstance(self, other.__class__):
            return self.expressions == other.expressions
        return False


class ExprLoop(ExprAST):
    def __init__(self, block: ExprBlock):
        self.block = block

    def __repr__(self):
        return '[' + str(self.block) + ']'

    def __eq__(self, other):
        if isinstance(self, other.__class__):
            return self.block == other.block
        return False


class ExprPrint(ExprAST):

    def __repr__(self):
        return Token.PRINT.value

    def __eq__(self, other):
        return isinstance(self, other.__class__)


class ExprScan(ExprAST):

    def __repr__(self):
        return Token.SCAN.value

    def __eq__(self, other):
        return isinstance(self, other.__class__)


class Parser:
    tokens: List[Token]
    current_token: chr
    tokens_position = 1

    def __init__(self, tokens: List[Token]):
        self.tokens = tokens
        self.current_token = tokens[0]

    def get_next_token(self):
        self.current_token = self.tokens[self.tokens_position]
        self.tokens_position += 1

    def has_next_token(self):
        return self.tokens_position < len(self.tokens)

    def _parse_loop(self) -> ExprLoop:
        self.get_next_token()  # eat [
        block: ExprBlock = self._parse_block()
        if self.current_token != Token.R_BRACKET:
            log_error("Expected right bracket")
        return ExprLoop(block)

    def _parse_block(self) -> ExprBlock:
        expressions: List[ExprAST] = list()
        while True:
            if self.current_token == Token.R_BRACKET:
                break
            if self.current_token == Token.EOF:
                break
            expr = {
                Token.DEC_PTR: ExprChangePtr(-1),
                Token.INC_PTR: ExprChangePtr(1),
                Token.INC_VAL: ExprChangeValue(value=1),
                Token.DEC_VAL: ExprChangeValue(value=-1),
                Token.PRINT: ExprPrint(),
                Token.SCAN: ExprScan(),
            }.get(self.current_token)
            if self.current_token == Token.L_BRACKET:
                expr = self._parse_loop()

            expressions.append(expr)

            if not self.has_next_token():
                break
            self.get_next_token()
        return ExprBlock(expressions)

    def parse(self):
        parsed = self._parse_block()
        if self.current_token != Token.EOF:
            log_error("Something went wrong")
        return parsed
