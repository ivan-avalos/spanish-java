import uuid
import graphviz as gv
from dataclasses import dataclass
from typing import Optional, cast

from astree.graphable import Graphable
from astree.type import Type
from astree.ident import Ident
from astree.expr import Expr

# A global declaration.
#
#     entero a = 0;
@dataclass
class DeclGlobal(Graphable):
    ident: Ident
    _type: Type
    init: Expr

    def graph(self, dot: gv.Digraph, parent: str = None, edge: str = None) -> None:
        name = uuid.uuid1().hex
        dot.node(name, 'DeclGlobal')
        dot.edge(parent, name, label = edge)
        name_ident = uuid.uuid1().hex
        dot.node(name_ident, self.ident)
        dot.edge(name, name_ident, label = 'ident')
        if isinstance(self.init, Graphable):
            self.init.graph(dot, name, 'init')

# A function declaration.
#
#     funcion vacio main() { ... }
@dataclass
class DeclFunc(Graphable):
    ident: Ident
    prototype: Type
    body: Optional[Expr]

    def graph(self, dot: gv.Digraph, parent: str = None, edge: str = None) -> None:
        name = uuid.uuid1().hex
        dot.node(name, 'DeclFunc')
        dot.edge(parent, name, label = edge)
        name_ident = uuid.uuid1().hex
        dot.node(name_ident, self.ident)
        dot.edge(name, name_ident, label = 'ident')
        if isinstance(self.prototype, Graphable):
            self.prototype.graph(dot, name, 'prototype')
        if self.body and isinstance(self.body, Graphable):
            self.body.graph(dot, name, 'body')

# A Javañol declaration
Decl = DeclGlobal | DeclFunc
