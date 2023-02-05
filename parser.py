import abc
from abc import ABC
from typing import List

import llvmlite.ir
from llvmlite import ir

from lexer import Lexer, Token
from utils import log_error


class ExprAST(ABC):
    @abc.abstractmethod
    def codegen(self, builder: llvmlite.ir.IRBuilder, mem, ptr, putchar, getchar):
        pass


class ExprIncreasePtr(ExprAST):
    def codegen(self, builder, mem, ptr, putchar, getchar):
        ptr_addr = builder.load(ptr)
        new_addr = builder.gep(ptr_addr, [ir.Constant(ir.IntType(32), 1)])
        builder.store(new_addr, ptr)

    def __repr__(self):
        return Token.INC_PTR.value


class ExprDecreasePtr(ExprAST):

    def codegen(self, builder, mem, ptr, putchar, getchar):
        ptr_addr = builder.load(ptr)
        new_addr = builder.gep(ptr_addr, [ir.Constant(ir.IntType(32), -1)])
        builder.store(new_addr, ptr)

    def __repr__(self):
        return Token.DEC_PTR.value


class ExprIncreaseValue(ExprAST):

    def codegen(self, builder, mem, ptr, putchar, getchar):
        ptr_addr = builder.load(ptr)
        value = builder.load(ptr_addr)
        res = builder.add(value, ir.Constant(ir.IntType(32), 1))
        builder.store(res, ptr_addr)

    def __repr__(self):
        return Token.INC_VAL.value


class ExprDecreaseValue(ExprAST):

    def codegen(self, builder, mem, ptr, putchar, getchar):
        ptr_addr = builder.load(ptr)
        value = builder.load(ptr_addr)
        res = builder.add(value, ir.Constant(ir.IntType(32), -1))
        builder.store(res, ptr_addr)

    def __repr__(self):
        return Token.DEC_VAL.value


class ExprBlock(ExprAST):
    expressions = List[ExprAST]

    def __init__(self, expressions: List[ExprAST]):
        self.expressions = expressions

    def codegen(self, builder, mem, ptr, putchar, getchar):
        for expr in self.expressions:
            expr.codegen(builder, mem, ptr, putchar, getchar)

    def __repr__(self):
        return str(self.expressions)


class ExprLoop(ExprAST):
    def __init__(self, block: ExprBlock):
        self.block = block

    def codegen(self, builder, mem, ptr, putchar, getchar):
        pass

    def __repr__(self):
        return '[' + str(self.block) + ']'


class ExprPrint(ExprAST):

    def __repr__(self):
        return Token.PRINT.value

    def codegen(self, builder, mem, ptr, putchar, getchar):
        ptr_addr = builder.load(ptr)
        value = builder.load(ptr_addr)
        builder.call(putchar, (value,))


class ExprScan(ExprAST):

    def codegen(self, builder, mem, ptr, putchar, getchar):
        tmp = builder.call(getchar, ())
        ptr_addr = builder.load(ptr)
        builder.store(tmp, ptr_addr)

    def __repr__(self):
        return Token.SCAN.value


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
                Token.DEC_PTR: ExprDecreasePtr(),
                Token.INC_PTR: ExprIncreasePtr(),
                Token.INC_VAL: ExprIncreaseValue(),
                Token.DEC_VAL: ExprDecreaseValue(),
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


if __name__ == '__main__':
    def test():
        test_code = Lexer(',++>++++[-<+>].').tokenize()
        parsed = Parser(test_code).parse()
        print(parsed)


    test()
