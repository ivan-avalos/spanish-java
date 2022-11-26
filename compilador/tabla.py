import json, os
from enum import Enum, auto
from dataclasses import dataclass
from typing import Any
# from more_itertools import seekable

from nanoiter import NanoIter

reservadas = [
    'booleano',
    'cadena',
    'caracter',
    'continuar',
    'detener',
    'entero',
    'funcion',
    'imprimir',
    'leer',
    'mientras',
    'retornar',
    'si',
    'sino',
    'vacio',
]

literales = [
    'BOOLEAN_LIT',
    'CHAR_LIT',
    'DOUBLE_LIT',
    'INT_LIT',
    'STRING_LIT'
]

tokens = reservadas + literales + [
    '{', '}', '(', ')', ',', '\'',
    '"', ';', '=', '*', '/', '+',
    '-', '>', '<', '>=', '<=', '&&',
    '||', '==', '!='
]

class Token(Enum):
    BOOLEAN = 'booleano'
    CHAR = 'caracter'
    DOUBLE = 'doble'
    ELSE = 'sino'
    IDENT = 'IDENT'
    IF = 'si'
    INT = 'entero'
    PRINT = 'imprimir'
    READ = 'leer'
    BREAK = 'detener'
    CONTINUE = 'continuar'
    RETURN = 'retornar'
    STRING = 'cadena'
    VOID = 'vacio'
    FUNCTION = 'funcion'
    WHILE = 'mientras'
    BOOLEAN_LIT = 'BOOLEAN_LIT'
    INT_LIT = 'INT_LIT'
    CHAR_LIT = 'CHAR_LIT'
    STRING_LIT = 'STRING_LIT'
    L_BRACKET = '{'
    R_BRACKET = '}'
    L_PAREN = '('
    R_PAREN = ')'
    COMMA = ','
    SQUOTE = '\''
    DQUOTE = '"'
    SEMICOLON = ';'
    EQUAL = '='
    TIMES = '*'
    SLASH = '/'
    PLUS = '+'
    MINUS = '-'
    GT = '>'
    LT = '<'
    GEQ = '>='
    LEQ = '<='
    AND = '&&'
    OR = '||'
    EQEQ = '=='
    NOTEQ = '!='
    EOF = 'EOF'



@dataclass
class LexToken:
    tipo: Token
    nombre: str
    valor: Any
    numlinea: int

    def __str__(self):
        return "LexToken(%s,%s,%s,%i)" % (
            self.tipo.name, self.nombre, self.valor, self.numlinea
        )

class TablaLex:
    def __init__(self):
        self.tabla = []

    def insertar(self, tok: LexToken):
        self.tabla.append(tok)

    def buscar(self, nombre: str):
        return [t for t in self.tabla if t.nombre == nombre][0]

    def iterar(self):
        return NanoIter(self.tabla)

    def actualizar(self, nombre: str, tok: LexToken):
        for i, t in enumerate(self.tabla):
            if t.nombre == nombre:
                self.tabla[i] = tok
                return

    def exportar(self, output_file):
        data = []
        for t in self.tabla:
            data.append({
                'tipo': t.tipo.value,
                'nombre': t.nombre,
                'valor': t.valor,
                'numlinea': t.numlinea
            })
        output = json.dumps(data)
        if os.path.exists(output_file):
            os.remove(output_file)
        with open(output_file, 'w+') as f:
            f.truncate(0)
            f.write(output)

    def importar(self, input_file):
        with open(input_file, 'r') as f:
            data = json.loads(f.read())
            for t in data:
                self.insertar(LexToken(Token(t['tipo']),
                                       t['nombre'],
                                       t['valor'],
                                       t['numlinea']))

    def __str__(self):
        output = ""
        for t in self.tabla:
            output += str(t) + "\n"
        return output
