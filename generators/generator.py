import abc

from parser import ExprLoop, ExprIncreaseValue, ExprBlock, ExprScan, ExprPrint, ExprDecreasePtr, ExprDecreaseValue, \
    ExprIncreasePtr, ExprAST


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
        elif isinstance(expr, ExprIncreasePtr):
            self._visitIncreasePtr(builder, expr)
        elif isinstance(expr, ExprDecreasePtr):
            self._visitDecreasePtr(builder, expr)
        elif isinstance(expr, ExprIncreaseValue):
            self._visitIncreaseValue(builder, expr)
        elif isinstance(expr, ExprDecreaseValue):
            self._visitDecreaseValue(builder, expr)
        elif isinstance(expr, ExprLoop):
            self._visitLoop(builder, expr)
        elif isinstance(expr, ExprPrint):
            self._visitPrint(builder, expr)
        elif isinstance(expr, ExprScan):
            self._visitScan(builder, expr)
        else:
            raise RuntimeError(f"Unknown expression {expr}")

    @abc.abstractmethod
    def _visitIncreasePtr(self, builder, expr: ExprIncreasePtr):
        pass

    @abc.abstractmethod
    def _visitDecreasePtr(self, builder, expr: ExprDecreasePtr):
        pass

    @abc.abstractmethod
    def _visitDecreaseValue(self, builder, expr: ExprDecreaseValue):
        pass

    @abc.abstractmethod
    def _visitIncreaseValue(self, builder, expr: ExprIncreaseValue):
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
