from enum import Enum
from tabla import LexToken, TablaLex, tokens
from arbol import Arbol, Nodo
from shared import Control
from pprint import pprint
from errors import Error
from typing import NoReturn
from more_itertools import seekable

from nanoiter import NanoIter
from tabla import TablaLex, Token
from errors import Error

class BaseParser:
    def __init__(self, iterador: NanoIter):
        self.iterador: NanoIter = iterador

    def want(self, *want: Token) -> (LexToken | Error):
        '''Requires the next token to have a matching ltok. Returns
        that token, or an error.

        '''
        tok: LexToken = self.lex()
        if len(want) == 0:
            return tok
        for w in want:
            if tok.tipo == w:
                return tok

        return Error.syntax(tok.tipo, want, tok.numlinea)

    def _try(self, *want: Token) -> (LexToken | NoReturn):
        '''Looks for a matching ltok from the lexer, and if not
        present, unlexes the token and returns void. If found, the
        token is consumed from the lexer and is returned.

        '''
        tok: LexToken = self.lex()
        if len(want) == 0:
            return tok
        for w in want:
            if tok.tipo == w:
                return tok
        self.unlex()

    def peek(self, *want: Token) -> (LexToken | NoReturn):
        '''Looks for a matching ltok from the lexer, unlexes the
        token, and returns it; or void if it was not an ltok.

        '''
        tok: LexToken = self.iterador.peek()
        if len(want) == 0:
            return tok
        for w in want:
            if tok.tipo == w:
                return tok

    def lex(self):
        return self.iterador.next()

    def unlex(self):
        self.iterador.back()

    def synassert(self, cond: bool, msg: str) -> (Error | NoReturn):
        '''Returns a syntax error if cond is false and void
        otherwise.

        '''
        if not cond:
            return Error(msg = msg)
