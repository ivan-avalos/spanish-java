#!/bin/env python
# -*- coding: utf-8 -*-
# Copyright (C) 2022  Iván Alejandro Ávalos Díaz <avalos@disroot.org>
#                     Edgar Alexis López Martínez <edgarmlmp@gmail.com>
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
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
        name_type = uuid.uuid1().hex
        dot.node(name_type, self._type.value.value)
        dot.edge(name, name_type, label = 'type')
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
