from enum import Enum
from symbol import LexToken, TablaLex, tokens

op_compuestos = ['>=', '<=', '==', '!=', '&&', '||', '++', '--']
op_simples_a = ['=', '+', '-', '&', '|'] # pueden ir al final del op compuesto
op_simples_b = ['!', '<', '>']           # solo pueden ir al inicio del op compuesto
op_simples = op_simples_a + op_simples_b

class Selector(Enum):
    NINGUNO = 0
    STRING_LIT = 1
    CHAR_LIT = 2
    ID_RESERVADA = 3
    COMMENT = 4

class Control(Enum):
    SIGUIENTE = 0
    REPETIR = 1
    ERROR = 2

class Lexer:
    tabla = TablaLex()
    selector = Selector.NINGUNO
    recol_string = ''
    recol_caracter = ''
    recol_comentario = ''
    recol_operador = ''
    recol_ident = ''

    def inicio_lexer(self, data):
        for c in data + "\n":
            r = self.procesar(c)
            if r == 2: return
            while r != Control.SIGUIENTE:
                print ('r = ' + str(r))
                r = self.procesar(c)
                if r == Control.ERROR: return

        # Imprimir tabla de símbolos
        print (str(self.tabla))

    def procesar(self, c):
        if c != "\t" and c != "\n":
            print (c + ' (' + str(self.selector) + ')')

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
            elif (c == '{' or c == '}' or c == '(' or c == ')' or
                  c == ',' or c == '.' or c == ';' or (c == '*' and self.recol_comentario == '')):
                self.tabla.insertar(LexToken(c, None, None, 1))
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
                    self.tabla.insertar(LexToken(rc, None, None, 1))
                    self.recol_operador = ''
                    return Control.SIGUIENTE
                else:
                    # Operador simple
                    self.tabla.insertar(LexToken(self.recol_operador, None, None, 1))
                    if c in op_simples:
                        self.tabla.insertar(LexToken(c, None, None, 1))
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

        return Control.SIGUIENTE

    def procesar_cadena(self, c):
        if c == '"':
            self.tabla.insertar(LexToken('STRING_LIT', None, self.recol_string, 1))
            self.selector = Selector.NINGUNO
            self.recol_string = ''
        else:
            self.recol_string += c
        return Control.SIGUIENTE

    def procesar_caracter(self, c):
        if len(self.recol_caracter) > 1:
            print ('Error: más de un caracter en una literal de caracter')
            return Control.ERROR
        if c == '\'':
            if len(self.recol_caracter) == 0:
                print ('Error: literal de caracter vacía')
                return Control.ERROR
            self.tabla.insertar(LexToken('CHAR_LIT', None, self.recol_caracter, 1))
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
            if self.recol_ident == 'booleano':
                self.tabla.insertar(LexToken('BOOLEAN', None, None, 1))
            elif self.recol_ident == 'detener':
                self.tabla.insertar(LexToken('BREAK', None, None, 1))
            elif self.recol_ident == 'byte':
                self.tabla.insertar(LexToken('BYTE', None, None, 1))
            elif self.recol_ident == 'caracter':
                self.tabla.insertar(LexToken('CHAR', None, None, 1))
            elif self.recol_ident == 'doble':
                self.tabla.insertar(LexToken('DOUBLE', None, None, 1))
            elif self.recol_ident == 'sino':
                self.tabla.insertar(LexToken('ELSE', None, None, 1))
            elif self.recol_ident == 'porcada':
                self.tabla.insertar(LexToken('FOR', None, None, 1))
            elif self.recol_ident == 'si':
                self.tabla.insertar(LexToken('IF', None, None, 1))
            elif self.recol_ident == 'entero':
                self.tabla.insertar(LexToken('INT', None, None, 1))
            elif self.recol_ident == 'imprimir':
                self.tabla.insertar(LexToken('PRINT', None, None, 1))
            elif self.recol_ident == 'leer':
                self.tabla.insertar(LexToken('READ', None, None, 1))
            elif self.recol_ident == 'retorna':
                self.tabla.insertar(LexToken('RETURN', None, None, 1))
            elif self.recol_ident == 'vacio':
                self.tabla.insertar(LexToken('VOID', None, None, 1))
            elif self.recol_ident == 'mientras':
                self.tabla.insertar(LexToken('WHILE', None, None, 1))
            elif self.recol_ident == 'verdadero':
                self.tabla.insertar(LexToken('BOOLEAN_LIT', None, True, 1))
            elif self.recol_ident == 'falso':
                self.tabla.insertar(LexToken('BOOLEAN_LIT', None, False, 1))
            else:
                self.tabla.insertar(LexToken('IDENT', self.recol_ident, None, 1))
            self.recol_ident = ''
            self.selector = Selector.NINGUNO
            return Control.REPETIR
        return Control.SIGUIENTE
