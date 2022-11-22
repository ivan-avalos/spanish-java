import json, os
from enum import Enum
from dataclasses import dataclass
from typing import Any

reservadas = [
    'BOOLEAN',
    'BREAK',
    'CHAR',
    'DOUBLE',
    'ELSE',
    'FOR'
    'IDENT',
    'IF',
    'INT',
    'PRINT',
    'READ',
    'RETURN',
    'STRING',
    'VOID',
    'WHILE'
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
    '||', '==', '!=', '++', '--', '//'
]

@dataclass
class LexToken:
    tipo: str
    nombre: str
    valor: Any
    numlinea: int

    def __str__(self):
        return "LexToken(%s,%s,%s,%i)" % (
            self.tipo, self.nombre, self.valor, self.numlinea
        )

class TablaLex:
    def __init__(self):
        self.tabla = []

    def insertar(self, tok: LexToken):
        self.tabla.append(tok)

    def buscar(self, nombre: str):
        return [t for t in self.tabla if t.nombre == nombre][0]

    def actualizar(self, nombre: str, tok: LexToken):
        for i, t in enumerate(self.tabla):
            if t.nombre == nombre:
                self.tabla[i] = tok
                return

    def exportar(self, output_file):
        data = []
        for t in self.tabla:
            data.append({
                'tipo': t.tipo,
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
                self.insertar(LexToken(t['tipo'],
                                       t['nombre'],
                                       t['valor'],
                                       t['numlinea']))

    def __str__(self):
        output = ""
        for t in self.tabla:
            output += str(t) + "\n"
        return output
