from llvmlite import ir
from ctypes import CFUNCTYPE, c_int
from llvm_helpers import create_execution_engine, compile_ir
from parser import ExprLoop, ExprIncreaseValue, ExprPrint, ExprScan, ExprDecreaseValue, ExprDecreasePtr, \
    ExprIncreasePtr, ExprBlock, ExprAST
from utils import log_error
from generators.generator import ASTGenerator


class CGenerator(ASTGenerator):

    def __init__(self):
        self.builder = []

    def generate(self, ast: ExprBlock):
        self.builder += "#include <stdio.h>\n" \
                        "int mem[3000];int main(){int*p;p = mem;"
        self._visit(self.builder, ast)
        self.builder += "return 0;}"

    def run(self):
        print("".join(self.builder))

    def _visitIncreasePtr(self, builder, expr: ExprIncreasePtr):
        builder += "p++;"

    def _visitDecreasePtr(self, builder, expr: ExprDecreasePtr):
        builder += "p--;"

    def _visitDecreaseValue(self, builder, expr: ExprDecreaseValue):
        builder += "(*p)--;"

    def _visitIncreaseValue(self, builder, expr: ExprIncreaseValue):
        builder += "(*p)++;"

    def _visitLoop(self, builder, expr: ExprLoop):
        builder += "while((*p)!=0){"
        self._visitBlock(builder, expr.block)
        builder += "}"

    def _visitBlock(self, builder, expr: ExprBlock):
        for inner_expression in expr.expressions:
            self._visit(builder, inner_expression)

    def _visitScan(self, builder, expr: ExprScan):
        builder += "*p=getchar();"

    def _visitPrint(self, builder, expr: ExprPrint):
        builder += "putchar(*p);"
