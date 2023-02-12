from itertools import zip_longest
from typing import cast

from optimisers.optimiser import Optimiser
from parser import ExprAST, ExprBlock, ExprChangePtr, ExprPrint, ExprScan, \
    ExprChangeValue, ExprLoop


class OperationFuser(Optimiser):

    def optimise(self, ast: ExprAST) -> bool:
        changed = False
        if isinstance(ast, ExprBlock):
            changed |= self._optimiseBlock(ast)
            for expression in ast.expressions:
                changed |= self.optimise(expression)
        if isinstance(ast, ExprLoop):
            changed |= self.optimise(ast.block)
        return changed

    def _can_be_fused(self, expr1, expr2):
        if isinstance(expr1, ExprChangeValue) and isinstance(expr2, ExprChangeValue):
            return True
        if isinstance(expr1, ExprChangeValue) and \
                isinstance(expr2, ExprChangeValue) and \
                expr1.offset == expr2.offset:
            return True
        return False

    def _fuse_opartions(self, expr, cumulated):
        if isinstance(expr, ExprChangePtr):
            expr.offset += cumulated
            return expr
        if isinstance(expr, ExprChangeValue):
            expr.value += cumulated
            return expr
        raise RuntimeError("Operation can't be fused")

    def _optimiseBlock(self, expr: ExprBlock) -> bool:
        optimised = []
        cumulated = 0
        changed = False
        for expr1, expr2 in zip_longest(expr.expressions, expr.expressions[1:]):
            if self._can_be_fused(expr1, expr2):
                cumulated += expr1.value
            else:
                if cumulated != 0:
                    optimised.append(self._fuse_opartions(expr1, cumulated))
                    changed = True
                else:
                    optimised.append(expr1)
                cumulated = 0
        expr.expressions = optimised
        return changed


def test():
    optimiser = OperationFuser()
    ast = ExprBlock(
        [ExprChangePtr(1), ExprChangePtr(1), ExprChangePtr(1),
         ExprChangePtr(-1), ExprChangePtr(-3),
         ExprPrint(),
         ExprChangePtr(1), ExprChangePtr(1),
         ExprChangeValue(offset=1, value=1), ExprChangeValue(offset=1, value=1), ExprChangeValue(offset=1, value=1),
         ExprChangeValue(offset=2, value=1),
         ExprChangeValue(offset=1, value=1),
         ExprChangeValue(value=1), ExprChangeValue(value=1), ExprChangeValue(value=1),
         ExprScan(),
         ExprLoop(
             ExprBlock([
                 ExprPrint(),
                 ExprChangeValue(value=1), ExprChangeValue(value=2), ExprChangeValue(value=1),
                 ExprChangePtr(1), ExprChangePtr(1),
             ])
         ),
         ExprChangeValue(value=-1), ExprChangeValue(value=-1), ExprChangeValue(value=-1), ])
    changed = optimiser.optimise(ast)
    print(ast, changed)


def test2():
    optimiser = OperationFuser()
    ast = ExprBlock([
        ExprChangeValue(value=-1), ExprChangeValue(value=-1), ExprChangeValue(value=-1),
    ])
    changed = optimiser.optimise(ast)
    print(ast, changed)


if __name__ == '__main__':
    test2()
