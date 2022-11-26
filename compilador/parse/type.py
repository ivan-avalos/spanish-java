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
from typing import List

from parse.base import BaseParser
from lexer import LexToken, Token
from astree.type import Type, BuiltinType, FuncType, FuncParam
from errors import Error

class ParseType:
    def __init__(self, parser: BaseParser):
        self.parser = parser

    def _type(self) -> (Type | Error):
        types = [Token.BOOLEAN, Token.CHAR, Token.INT, Token.STRING, Token.VOID]
        tok = self.parser.want(*types)
        if type(tok) is Error:
            return tok
        return BuiltinType(tok.tipo)

    def prototype(self, _type: Type) -> (FuncType | Error):
        params: List[FuncParam] = []

        # (
        tok = self.parser.want(Token.L_PAREN)
        if type(tok) is Error:
            return tok
        
        while not self.parser._try(Token.R_PAREN):
            
            # Tipo
            __type = ParseType(self.parser)._type()
            if type(__type) is Error:
                return __type

            # Identificador
            name = self.parser.want(Token.IDENT)
            if type(name) is Error:
                return name

            params.append(FuncParam(name = name.nombre,
                                    _type = __type))

            # ,
            if self.parser._try(Token.COMMA):
                continue

            # )
            if self.parser._try(Token.R_PAREN):
                break

        return FuncType(result = _type,
                        params = params)
