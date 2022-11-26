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
import sys, pickle
import graphviz as gv
from pprint import pprint

from tabla import TablaLex
from errors import Error
from parse.base import BaseParser
from parse.unit import ParseUnit

class Parser:
    def __init__(self, input_file: str):
        self.input_file = input_file
        self.tabla = TablaLex()
        self.tabla.importar(input_file + '.tab')
        self.iterador = self.tabla.iterar()

    def inicio(self):
        parser = BaseParser(self.iterador)
        unit = ParseUnit(parser).unit()
        if type(unit) is Error:
            print (unit.message, file=sys.stderr)
            return 1

        # Renderizar AST
        dot = gv.Digraph()
        dot.attr('node', fontname='monospace')
        unit.graph(dot)
        dot.render(self.input_file + '.gv')

        # Serializar AST
        with open(self.input_file + '.ast', 'wb') as f:
            pickle.dump(unit, f)
        
        return 0
