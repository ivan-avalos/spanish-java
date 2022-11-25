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

            params.append(FuncParam(name = name,
                                    _type = __type))

            # ,
            if self.parser._try(Token.COMMA):
                continue

            # )
            if self.parser._try(Token.R_PAREN):
                break

        return FuncType(result = _type,
                        params = params)
