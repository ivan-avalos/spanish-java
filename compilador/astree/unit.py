import uuid
import graphviz as gv
from dataclasses import dataclass
from typing import List

from astree.graphable import Graphable
from astree.decl import Decl

# A single compilation unit, representing all of the members of a namespace.
@dataclass
class Unit(Graphable):
    decls: List[Decl]

    def graph(self, dot: gv.Digraph, parent: str = None, edge: str = None) -> None:
        name = uuid.uuid1().hex
        dot.node(name, 'Unit')
        if parent:
            dot.edge(name, parent, label = edge)
        for d in self.decls:
            if isinstance(d, Graphable):
                d.graph(dot, name, 'decl')
