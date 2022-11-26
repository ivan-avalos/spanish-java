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
