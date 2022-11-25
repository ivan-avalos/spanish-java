import sys
from pprint import pprint

from tabla import TablaLex
from errors import Error
from parse.base import BaseParser
from parse.unit import ParseUnit

class Parser:
    def __init__(self, input_file: str):
        self.tabla = TablaLex()
        self.tabla.importar(input_file + '.tab')
        self.iterador = self.tabla.iterar()

    def inicio(self):
        parser = BaseParser(self.iterador)
        unit = ParseUnit(parser).unit()
        if type(unit) is Error:
            print (unit.message, file=sys.stderr)
            return 1

        pprint(unit)
        return 0
