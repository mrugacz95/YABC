from optimisers.optimiser import Optimiser
from parser import ExprAST, ExprBlock, ExprLoop, ExprChangePtr, \
    ExprChangeValue, ExprPrint
from utils import window


class OffsetFuser(Optimiser):
    def optimise(self, ast: ExprAST) -> bool:
        changed = False
        if isinstance(ast, ExprBlock):
            changed |= self._optimiseBlock(ast)
            for expression in ast.expressions:
                changed |= self.optimise(expression)
        elif isinstance(ast, ExprLoop):
            changed |= self.optimise(ast.block)
        return changed

    def _optimiseBlock(self, block: ExprBlock):
        changed = False
        optimised = []
        triples = list(window(block.expressions + [None, None],
                              3))  # todo change None to EmptyOperation
        i = 0
        while i < len(triples):
            (prev, mid, next) = triples[i]
            if isinstance(prev, ExprChangePtr) and \
                    isinstance(mid, ExprChangeValue) and \
                    isinstance(next, ExprChangePtr) and \
                    prev.offset == -next.offset:
                optimised.append(
                    ExprChangeValue(offset=prev.offset + mid.offset,
                                    value=mid.value))
                i += 3
                changed = True
            else:
                optimised.append(prev)
                i += 1
        if changed:
            block.expressions = optimised
        return changed


def test():
    # +++++++++[>>+++++++++<<-]>>.
    source = ExprBlock([
        ExprChangeValue(9),
        ExprLoop(ExprBlock([
            ExprChangePtr(2),
            ExprChangeValue(offset=0, value=9),
            ExprChangePtr(-2),
            ExprChangeValue(offset=0, value=-1)
        ])),
        ExprChangePtr(2),
        ExprPrint()
    ])
    changed = OffsetFuser().optimise(source)
    print(source, changed)


if __name__ == '__main__':
    test()
