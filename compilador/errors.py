import sys

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

    def __init__(self, error, numlinea):
        print("Error en línea %d: %s" % (numlinea, self.errors[error]), file=sys.stderr)
