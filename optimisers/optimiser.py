import abc

from parser import ExprAST


class Optimiser(abc.ABC):
    @abc.abstractmethod
    def optimise(self, ast: ExprAST) -> bool:
        pass
