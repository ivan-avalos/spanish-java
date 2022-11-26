import graphviz as gv
from typing import Protocol, runtime_checkable
from abc import abstractmethod

@runtime_checkable
class Graphable(Protocol):
    @abstractmethod
    def graph(self, dot: gv.Digraph, parent: str = None, edge: str = None) -> None:
        raise NotImplementedError
