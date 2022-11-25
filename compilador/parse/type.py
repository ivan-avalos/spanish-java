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

    def prototype(self) -> (FuncType | Error):
        params: List[FuncParam] = []

        # Tipo
        tok = ParseType(self.parser)._type()
        if type(tok) is Error:
            return tok
        _type = tok

        # (
        tok = self.parser.want(Token.L_PAREN)
        if type(tok) is Error:
            return tok
        while True:
            tok = self.parser._try(Token.R_PAREN)
            if not tok:
                break

            # Tipo
            tok = ParseType(self.parser)._type()
            if type(tok) is Error:
                return tok
            __type: Type = tok

            # Identificador
            tok = self.parser.want(Token.IDENT)
            if type(tok) is Error:
                return tok
            name: str = tok

            params.append(FuncParam(name = name,
                                    _type = __type))

            # ,
            tok = self.parser._try(Token.COMMA)
            if not tok:
                continue

            # )
            tok = self.parser.want(Token.R_PAREN)
            if type(tok) is Error:
                return tok

        return FuncType(result = _type,
                        params = params)
