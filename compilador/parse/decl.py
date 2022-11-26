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
from typing import List, cast, Optional
from more_itertools import peekable

from tabla import Token, LexToken
from parse.base import BaseParser
from errors import Error
from parse.type import ParseType
from parse.ident import ParseIdent
from parse.expr import ParseExpr, Expr
from astree.decl import DeclGlobal, DeclFunc, Decl

class ParseDecl:
    def __init__(self, parser: BaseParser):
        self.parser = parser

    def decl_global(self) -> (DeclGlobal | Error):
        # Tipo
        _type = ParseType(self.parser)._type()
        if type(_type) is Error:
            return _type

        # Identificador
        ident = ParseIdent(self.parser).ident()
        if type(ident) is Error:
            return ident

        # =
        init: Optional[Expr] = None
        eq = self.parser._try(Token.EQUAL)
        if eq:
            # Expresión
            init = ParseExpr(self.parser).expr()
            if type(init) is Error:
                return init

        return DeclGlobal(ident = ident,
                          _type = _type,
                          init = init)

    def decl_func(self) -> (DeclFunc | Error):
        # funcion
        tok = self.parser.want(Token.FUNCTION)
        if type(tok) is Error:
            return tok

        # Tipo
        _type = ParseType(self.parser)._type()
        if type(_type) is Error:
            return _type

        # Identificador
        ident = ParseIdent(self.parser).ident()
        if type(ident) is Error:
            return ident

        # Prototipo
        proto = ParseType(self.parser).prototype(_type)
        if type(proto) is Error:
            return proto

        init = ParseExpr(self.parser).compound_expr()
        if type(init) is Error:
            return init

        return DeclFunc(ident = ident,
                        prototype = proto,
                        body = init)

    # Parses a declaration.
    def decl(self) -> (Decl | Error):
        toks = [Token.BOOLEAN, Token.CHAR, Token.INT, Token.STRING, Token.VOID, Token.FUNCTION]
        _next = self.parser.want(*toks)
        decl: Optional[Decl] = None
        if type(_next) is Error:
            return _next
        elif _next.tipo is Token.FUNCTION:
            self.parser.unlex()
            decl = self.decl_func()
        else:
            self.parser.unlex()
            decl = self.decl_global()

        if type(decl) is Error:
            return decl

        # ;
        semicolon = self.parser.want(Token.SEMICOLON)
        if type(semicolon) is Error:
            return semicolon

        return decl

    # Parses the declarations for a sub-parser.
    def decls(self) -> (List[Decl] | Error):
        decls: List[Decl] = []
        while not self.parser.peek(Token.EOF):
            decl = self.decl()
            if type(decl) is Error:
                return decl
            decls.append(decl)

        return decls
