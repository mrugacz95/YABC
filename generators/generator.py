import abc

from parser import ExprLoop, ExprBlock, ExprScan, ExprPrint, ExprChangePtr, ExprAST, ExprChangeValue


class ASTGenerator:
    @abc.abstractmethod
    def generate(self, ast: ExprBlock):
        pass

    @abc.abstractmethod
    def run(self):
        pass

    def _visit(self, builder, expr: ExprAST):
        if isinstance(expr, ExprBlock):
            self._visitBlock(builder, expr)
        elif isinstance(expr, ExprChangePtr):
            self._visitChangePtr(builder, expr)
        elif isinstance(expr, ExprChangeValue):
            self._visitChangeValue(builder, expr)
        elif isinstance(expr, ExprLoop):
            self._visitLoop(builder, expr)
        elif isinstance(expr, ExprPrint):
            self._visitPrint(builder, expr)
        elif isinstance(expr, ExprScan):
            self._visitScan(builder, expr)
        else:
            raise RuntimeError(f"Unknown expression {expr}")

    @abc.abstractmethod
    def _visitChangePtr(self, builder, expr: ExprChangePtr):
        pass

    @abc.abstractmethod
    def _visitChangeValue(self, builder, expr: ExprChangeValue):
        pass

    @abc.abstractmethod
    def _visitLoop(self, builder, expr: ExprLoop):
        pass

    @abc.abstractmethod
    def _visitBlock(self, builder, expr: ExprBlock):
        pass

    @abc.abstractmethod
    def _visitScan(self, builder, expr: ExprScan):
        pass

    @abc.abstractmethod
    def _visitPrint(self, builder, expr: ExprPrint):
        pass
