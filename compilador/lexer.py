from enum import Enum
from tabla import LexToken, TablaLex, tokens
from parser import Parser
from shared import Control
from errors import Error

op_compuestos = ['>=', '<=', '==', '!=', '&&', '||', '++', '--']
op_simples_a = ['=', '+', '-', '&', '|'] # pueden ir al final del op compuesto
op_simples_b = ['!', '<', '>']           # solo pueden ir al inicio del op compuesto
op_simples = op_simples_a + op_simples_b
otros_tokens = ['{', '}', '(', ')', ',', '.', ';']
reservadas = {
    'booleano': 'BOOLEAN',
    'detener': 'BREAK',
    'cadena': 'STRING',
    'caracter': 'CHAR',
    'sino': 'ELSE',
    'porcada': 'FOR',
    'si': 'IF',
    'entero': 'INT',
    'imprimir': 'PRINT',
    'leer': 'READ',
    'retorna': 'RETURN',
    'vacio': 'VOID',
    'mientras': 'WHILE'
}

class Selector(Enum):
    NINGUNO = 0
    STRING_LIT = 1
    CHAR_LIT = 2
    ID_RESERVADA = 3
    COMMENT = 4
    ENTERO = 5

class Lexer:
    def __init__(self, data, input_file):
        self.tabla = TablaLex()
        self.numlinea = 1
        self.selector = Selector.NINGUNO
        self.recol_string = ''
        self.recol_caracter = ''
        self.recol_comentario = ''
        self.recol_operador = ''
        self.recol_ident = ''
        self.recol_entero = ''
        self.data = data
        self.tabla_file = None
        if input_file:
            self.tabla_file = input_file + '.tab'

    def inicio(self):
        for l in self.data.splitlines():
            for c in l + "\n":
                r = self.procesar(c)
                if r == Control.ERROR: exit(1)
                while r != Control.SIGUIENTE:
                    r = self.procesar(c)
                    if r == Control.ERROR: exit(1)
            self.numlinea += 1

        # Imprimir tabla de símbolos
        if self.tabla_file:
            self.tabla.exportar(self.tabla_file)
        Parser(self.tabla).inicio()
        

    def procesar(self, c):
        # if c != "\t" and c != "\n":
        #    print (c + ' (' + str(self.selector) + ')')

        if self.selector == Selector.NINGUNO:
            # Entrada a string
            if c == '"':
                self.selector = Selector.STRING_LIT
                return Control.SIGUIENTE
            # Entrada a caracter
            elif c == '\'':
                self.selector = Selector.CHAR_LIT
                return Control.SIGUIENTE
            # Entrada a id o palabra reservada
            elif c.isalpha() or c == '_':
                self.selector = Selector.ID_RESERVADA
            # Entrada a entero
            elif c.isdigit():
                self.selector = Selector.ENTERO
            # Entrada a comentario
            elif c == '/':
                self.recol_comentario = '/'
            # Entrada a operador (simple o compuesto)
            elif c in op_simples_a and self.recol_operador == '':
                self.recol_operador = c
                return Control.SIGUIENTE
            # Entrada a operador (simple)
            elif c in op_simples_b:
                self.recol_operador = c
                return Control.SIGUIENTE
            # Entrada a tokens simples
            elif c in otros_tokens or (c == '*' and self.recol_comentario == ''):
                self.insertar_tabla(c, None, None)
                return Control.SIGUIENTE

            # Apertura de comentario
            if self.recol_comentario == '/' and c == '*':
                self.selector = Selector.COMMENT
                self.recol_comentario = ''
                return Control.SIGUIENTE

            # Apertura de operador compuesto
            if len(self.recol_operador) > 0:
                rc = self.recol_operador + c
                if rc in op_compuestos:
                    # Operador compuesto
                    self.insertar_tabla(rc, None, None)
                    self.recol_operador = ''
                    return Control.SIGUIENTE
                else:
                    # Operador simple
                    self.insertar_tabla(self.recol_operador, None, None)
                    if c in op_simples:
                        self.insertar_tabla(c, None, None)
                    self.recol_operador = ''
                    return Control.SIGUIENTE

        # Cadenas de texto
        if self.selector == Selector.STRING_LIT:
            return self.procesar_cadena(c)
            
        # Caracteres
        if self.selector == Selector.CHAR_LIT:
            return self.procesar_caracter(c)

        # Comentarios
        if self.selector == Selector.COMMENT:
            return self.procesar_comentario(c)

        # Identificador o palabra reservada
        if self.selector == Selector.ID_RESERVADA:
            return self.procesar_identificador(c)

        # Enteros
        if self.selector == Selector.ENTERO:
            return self.procesar_entero(c)

        return Control.SIGUIENTE

    def procesar_cadena(self, c):
        if c == '"':
            self.insertar_tabla('STRING_LIT', None, self.recol_string)
            self.selector = Selector.NINGUNO
            self.recol_string = ''
        else:
            self.recol_string += c
        return Control.SIGUIENTE

    def procesar_caracter(self, c):
        if len(self.recol_caracter) > 1:
            Error('L_CAR_LARGO', self.numlinea)
            return Control.ERROR
        if c == '\'':
            if len(self.recol_caracter) == 0:
                Error('L_CAR_VACIO', self.numlinea)
                return Control.ERROR
            self.insertar_tabla('CHAR_LIT', None, self.recol_caracter)
            self.selector = Selector.NINGUNO
            self.recol_caracter = ''
        else:
            self.recol_caracter += c
        return Control.SIGUIENTE

    def procesar_comentario(self, c):
        if c == '*':
            self.recol_comentario = c
        elif self.recol_comentario == '*':
            if c == '/':
                self.selector = Selector.NINGUNO
                self.recol_comentario = ''
            else:
                self.recol_comentario = ''
        return Control.SIGUIENTE

    def procesar_identificador(self, c):
        if c.isalnum() or c == '_':
            self.recol_ident += c
        else:
            if self.recol_ident in reservadas.keys():
                self.insertar_tabla(reservadas[self.recol_ident], None, None)
            elif self.recol_ident == 'verdadero':
                self.insertar_tabla('BOOLEAN_LIT', None, True)
            elif self.recol_ident == 'falso':
                self.insertar_tabla('BOOLEAN_LIT', None, False)
            else:
                self.insertar_tabla('IDENT', self.recol_ident, None)
            self.recol_ident = ''
            self.selector = Selector.NINGUNO
            return Control.REPETIR
        return Control.SIGUIENTE

    def procesar_entero(self, c):
        if c.isdigit():
            self.recol_entero += c
        else:
            self.insertar_tabla('INT_LIT', None, int(self.recol_entero))
            self.recol_entero = ''
            self.selector = Selector.NINGUNO
            return Control.REPETIR
        return Control.SIGUIENTE

    def insertar_tabla(self, token, nombre, valor):
        self.tabla.insertar(LexToken(token, nombre, valor, self.numlinea))

            
        
