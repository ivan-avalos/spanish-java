from enum import Enum
from tabla import LexToken, TablaLex, tokens
from arbol import Arbol, Nodo
from shared import Control
from pprint import pprint
from errors import Error
from typing import NoReturn

from tabla import TablaLex, Token
from errors import Error

class Parser:
    def __init__(self, input_file: str):
        self.tabla = TablaLex()
        self.tabla.importar(input_file + '.tab')
        self.iterador = self.tabla.iterar()

    def inicio(self):
        tok = self.want(Token.STRING_LIT, Token.BOOLEAN_LIT)
        if type(tok) == Error:
            print(tok.message)
            return 1
        return 0

    ''' Requires the next token to have a matching ltok. Returns that
    token, or an error. '''
    def want(self, *want: Token) -> (Token | Error):
        tok: LexToken = next(self.iterador)
        if len(want) == 0:
            return tok
        for w in want:
            if tok.tipo == w:
                return tok
        return Error(got = tok.tipo, expects = want, numlinea = tok.numlinea)

     ''' Looks for a matching ltok from the lexer, and if not present,
     unlexes the token and returns void. If found, the token is
     consumed from the lexer and is returned. '''
    def _try(self, *want: Token) -> (Token | NoReturn):
        tok: LexToken = next(self.iterador)
        if len(want) == 0:
            return tok
        for w in want:
            if tok.tipo == w:
                return tok
        self.iterador.seek(-1)

    ''' Looks for a matching ltok from the lexer, unlexes the token,
    and returns it; or void if it was not an ltok. '''
    def peek(self, *want: Token) -> (Token | NoReturn):
        tok: LexToken = next(self.iterador)
        self.iterador.seek(-1)
        if len(want) == 0:
            return tok
        for w in want:
            if tok.tipo == w:
                return tok
