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
from tabla import Token, LexToken
from parse.base import BaseParser
from astree.ident import Ident
from errors import Error

class ParseIdent:
    def __init__(self, parser: BaseParser):
        self.parser = parser

    def ident(self) -> (Ident | Error):
        tok: LexToken = self.parser.want(Token.IDENT)
        if type(tok) is Error:
            return tok
        return tok.nombre
