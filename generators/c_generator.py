from generators.generator import ASTGenerator
from parser import ExprLoop, ExprPrint, ExprScan, ExprDecreasePtr, \
    ExprIncreasePtr, ExprBlock, ExprChangeValue


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
        builder += f"p+={expr.value};"

    def _visitDecreasePtr(self, builder, expr: ExprDecreasePtr):
        builder += f"p-={expr.value};"

    def _visitChangeValue(self, builder, expr: ExprChangeValue):
        if expr.value >= 0:
            sign = '+'
        else:
            sign = '-'
        builder += f"p[{expr.offset}]{sign}={abs(expr.value)};"

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
