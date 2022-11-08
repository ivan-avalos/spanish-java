from enum import Enum
from symbol import LexToken, TablaLex, tokens

op_compuestos = ['>=', '<=', '==', '!=', '&&', '||', '++', '--']
op_simples_a = ['=', '+', '-', '&', '|']
op_simples_b = ['!', '<', '>']
op_simples = op_simples_a + op_simples_b

class Lexer:
    tabla = TablaLex()
    selector = ''
    recol_string = ''
    recol_caracter = ''
    recol_comentario = ''
    recol_operador = ''
    recol_ident = ''

    def inicio_lexer(self, data):
        for c in data + "\n":
            r = self.procesar_caracter(c)
            if r == 2: return
            while r != 0:
                print ('r = ' + str(r))
                r = self.procesar_caracter(c)
                if r == 2: return

        # Imprimir tabla de símbolos
        print (str(self.tabla))

    # c => caracter
    # return 0 => siguiente caracter
    # return 1 => repetir caracter
    # return 2 => error
    def procesar_caracter(self, c):
        if c != "\t" and c != "\n":
            print (c + ' (' + self.selector + ')')

        if self.selector == '':
            # Entradas a tokens
            if c == '"':
                self.selector = 'STRING_LIT'
                return 0
            elif c == '\'':
                self.selector = 'CHAR_LIT'
                return 0
            elif c.isalpha() or c == '_':
                self.selector = 'ID/RESERVADA'
            elif c == '/':
                self.recol_comentario = '/'
            elif c in op_simples_a and self.recol_operador == '':
                self.recol_operador = c
                return 0
            elif c in op_simples_b:
                self.recol_operador = c
                return 0
            elif (c == '{' or c == '}' or c == '(' or c == ')' or
                  c == ',' or c == '.' or c == ';' or (c == '*' and self.recol_comentario == '')):
                self.tabla.insertar(LexToken(c, None, None, 1))
                return 0

            # Apertura de comentario
            if self.recol_comentario == '/' and c == '*':
                self.selector = 'COMMENT'
                self.recol_comentario = ''
                return 0

            # Apertura de operador compuesto
            if len(self.recol_operador) > 0:
                rc = self.recol_operador + c
                if rc in op_compuestos:
                    # Operador compuesto
                    self.tabla.insertar(LexToken(rc, None, None, 1))
                    self.recol_operador = ''
                    return 0
                else:
                    # Operador simple
                    self.tabla.insertar(LexToken(self.recol_operador, None, None, 1))
                    if c in op_simples:
                        self.tabla.insertar(LexToken(c, None, None, 1))
                    self.recol_operador = ''
                    return 0

        # Cadenas de texto
        if self.selector == 'STRING_LIT':
            if c == '"':
                self.tabla.insertar(LexToken('STRING_LIT', None, self.recol_string, 1))
                self.selector = ''
                self.recol_string = ''
            else:
                self.recol_string += c

        # Caracteres
        if self.selector == 'CHAR_LIT':
            if len(self.recol_caracter) > 1:
                print ('Error: más de un caracter en una literal de caracter')
                return 2
            if c == '\'':
                if len(self.recol_caracter) == 0:
                    print ('Error: literal de caracter vacía')
                    return 2
                self.tabla.insertar(LexToken('CHAR_LIT', None, self.recol_caracter, 1))
                self.selector = ''
                self.recol_caracter = ''
            else:
                self.recol_caracter += c

        # Comentarios
        if self.selector == 'COMMENT':
            if c == '*':
                self.recol_comentario = c
            elif self.recol_comentario == '*':
                if c == '/':
                    self.selector = ''
                    self.recol_comentario = ''
                else:
                    self.recol_comentario = ''

        # Identificador o palabra reservada
        if self.selector == 'ID/RESERVADA':
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
                self.selector = ''
                return 1
        return 0
