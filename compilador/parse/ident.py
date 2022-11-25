
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
