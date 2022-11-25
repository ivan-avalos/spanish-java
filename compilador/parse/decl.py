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

        return DeclFunc(ident = ident,
                        prototype = proto,
                        body = None)

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
