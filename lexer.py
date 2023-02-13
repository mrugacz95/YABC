from enum import Enum

from utils import log_error


class Token(Enum):
    INC_VAL = '+'
    DEC_VAL = '-'
    INC_PTR = '>'
    DEC_PTR = '<'
    PRINT = '.'
    SCAN = ','
    L_BRACKET = '['
    R_BRACKET = ']'
    EOF = 'eof'


class Lexer:

    def __init__(self, code: str):
        self.code = code

    def tokenize(self):
        tokenized = []
        open_brackets = 0
        for c in self.code:
            if c not in '<>[].,+-':
                continue
            if c == '[':
                open_brackets += 1
            if c == ']':
                open_brackets -= 1
            if open_brackets < 0:
                log_error("Loop end without beginning encountered.")
            tokenized.append(Token(c))
        if open_brackets > 0:
            log_error("Some closing brackets are missing.")
        tokenized.append(Token.EOF)
        return tokenized
