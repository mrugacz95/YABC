from itertools import zip_longest
from typing import cast

from optimisers.optimiser import Optimiser
from parser import ExprAST, ExprBlock, ExprIncreasePtr, ExprPrint, ExprCumulative, ExprDecreasePtr, ExprScan, \
    ExprIncreaseValue, ExprDecreaseValue, ExprLoop


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

    def _optimiseBlock(self, expr: ExprBlock) -> bool:
        optimised = []
        cumulated = 0
        changed = False
        for i, j in zip_longest(expr.expressions, expr.expressions[1:]):
            if isinstance(i, ExprCumulative) and type(i) is type(j):
                cumulated += i.value
            else:
                if cumulated > 0:
                    cast(ExprCumulative, i).value += cumulated
                    changed = True
                optimised.append(i)
                cumulated = 0
        expr.expressions = optimised
        return changed


def test():
    optimiser = OperationFuser()
    ast = ExprBlock([ExprIncreasePtr(), ExprIncreasePtr(), ExprIncreasePtr(),
                     ExprDecreasePtr(), ExprDecreasePtr(3),
                     ExprPrint(), ExprIncreasePtr(), ExprIncreasePtr(),
                     ExprIncreaseValue(), ExprIncreaseValue(), ExprIncreaseValue(), ExprIncreaseValue(),
                     ExprScan(),
                     ExprLoop(
                         ExprBlock([
                             ExprPrint(),
                             ExprIncreaseValue(), ExprIncreaseValue(2), ExprIncreaseValue(),
                             ExprIncreasePtr(), ExprIncreasePtr(),
                         ])
                     ),
                     ExprDecreaseValue(), ExprDecreaseValue(), ExprDecreaseValue(), ])
    changed = optimiser.optimise(ast)
    print(ast, changed)


if __name__ == '__main__':
    test()
