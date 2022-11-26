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
import sys
from typing import List

from tabla import Token

class Error:
    errors = {
        'L_CAR_LARGO': 'Más de un caracter en una literal de caracter',
        'L_CAR_VACIO': 'Literal de caracter vacía',
        'S_ESPERA_EXPR': 'Se esperaba una expresión',
        'S_ESPERA_IDENT': 'Se esperaba un identificador',
        'S_ESPERA_IDENT_O_LIT': 'Se esperaba un identificador o una literal',
        'S_ESPERA_OPER': 'Se esperaba un operador',
        'S_ESPERA_PC_O_IGUAL': 'Se esperaba `;` o `=`',
        'S_ESPERA_PC': 'Se esperaba `;`',
    }

    def __init__(self, msg: str = None, numlinea: int = None):
        if numlinea:
            self.message = "Error en la línea %d: %s" % (numlinea, msg)
        else:
            self.message = msg

    @classmethod
    def lex(self, error, numlinea: int):
        return Error("Error en línea %d: %s" % (numlinea, self.errors[error]))

    @classmethod
    def syntax(self, got: Token, expects: List[Token], numlinea: int):
        error = Error()
        strexp = ', '.join(['`%s\'' % e.value for e in expects])
        error.message = ("Error en la línea %d: se encontró `%s', pero se esperaba %s" %
                        (numlinea, got.value, strexp))
        return error
