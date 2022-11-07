from enum import Enum
from symbol import LexToken, TablaLex, tokens

def inicio_lexer(data):
    tabla = TablaLex()
    
    selector = ''
    recol_string = ''
    recol_caracter = ''
    recol_comentario = ''
    recol_operador = ''
    recol_ident = ''
    
    for c in data + "\n":
        # print (c + ' (' + selector + ')')
        
        if selector == '':
            # Entradas a tokens
            if c == '"':
                selector = 'STRING_LIT'
                continue
            elif c == '\'':
                selector = 'CHAR_LIT'
                continue
            elif c.isalpha() or c == '_':
                selector = 'ID/RESERVADA'
            elif c == '/':
                recol_comentario = '/'
            elif (c == '=' or c == '+' or c == '-' or c == '&' or c == '|') and recol_operador == '':
                recol_operador = c
                continue
            elif c == '!' or c == '<' or c == '>':
                recol_operador = c
                continue
            elif (c == '{' or c == '}' or c == '(' or c == ')' or
                  c == ',' or c == '.' or c == ';' or (c == '*' and recol_comentario == '')):
                tabla.insertar(LexToken(c, None, None, 1))
                continue

            # Apertura de comentario
            if recol_comentario == '/' and c == '*':
                selector = 'COMMENT'
                recol_comentario = ''
                continue

            # Apertura de operador compuesto
            if len(recol_operador) > 0:
                rc = recol_operador + c
                if (rc == '>=' or rc == '<=' or rc == '==' or rc == '!=' or
                    rc == '&&' or rc == '||' or rc == '++' or rc == '--'):
                    # Operador compuesto
                    tabla.insertar(LexToken(rc, None, None, 1))
                    recol_operador = ''
                    continue
                else:
                    # Operador simple
                    tabla.insertar(LexToken(recol_operador, None, None, 1))
                    recol_operador = ''
        
        # Cadenas de texto
        if selector == 'STRING_LIT':
            if c == '"':
                tabla.insertar(LexToken('STRING_LIT', None, recol_string, 1))
                selector = ''
                recol_string = ''
            else:
                recol_string += c

        # Caracteres
        if selector == 'CHAR_LIT':
            if len(recol_caracter) > 1:
                print ('Error: más de un caracter en una literal de caracter')
                break
            if c == '\'':
                if len(recol_caracter) == 0:
                    print ('Error: literal de caracter vacía')
                    break
                tabla.insertar(LexToken('CHAR_LIT', None, recol_caracter, 1))
                selector = ''
                recol_caracter = ''
            else:
                recol_caracter += c

        # Comentarios
        if selector == 'COMMENT':
            if c == '*':
                recol_comentario = c
            elif recol_comentario == '*':
                if c == '/':
                    selector = ''
                    recol_comentario = ''
                else:
                    recol_comentario = ''

        # Identificador o palabra reservada
        if selector == 'ID/RESERVADA':
            if c.isalnum() or c == '_':
                recol_ident += c
            else:
                if recol_ident == 'booleano':
                    tabla.insertar(LexToken('BOOLEAN', None, None, 1))
                elif recol_ident == 'detener':
                    tabla.insertar(LexToken('BREAK', None, None, 1))
                elif recol_ident == 'byte':
                    tabla.insertar(LexToken('BYTE', None, None, 1))
                elif recol_ident == 'caracter':
                    tabla.insertar(LexToken('CHAR', None, None, 1))
                elif recol_ident == 'doble':
                    tabla.insertar(LexToken('DOUBLE', None, None, 1))
                elif recol_ident == 'sino':
                    tabla.insertar(LexToken('ELSE', None, None, 1))
                elif recol_ident == 'porcada':
                    tabla.insertar(LexToken('FOR', None, None, 1))
                elif recol_ident == 'si':
                    tabla.insertar(LexToken('IF', None, None, 1))
                elif recol_ident == 'entero':
                    tabla.insertar(LexToken('INT', None, None, 1))
                elif recol_ident == 'imprimir':
                    tabla.insertar(LexToken('PRINT', None, None, 1))
                elif recol_ident == 'leer':
                    tabla.insertar(LexToken('READ', None, None, 1))
                elif recol_ident == 'retorna':
                    tabla.insertar(LexToken('RETURN', None, None, 1))
                elif recol_ident == 'vacio':
                    tabla.insertar(LexToken('VOID', None, None, 1))
                elif recol_ident == 'mientras':
                    tabla.insertar(LexToken('WHILE', None, None, 1))
                elif recol_ident == 'verdadero':
                    tabla.insertar(LexToken('BOOLEAN_LIT', None, True, 1))
                elif recol_ident == 'falso':
                    tabla.insertar(LexToken('BOOLEAN_LIT', None, False, 1))
                else:
                    tabla.insertar(LexToken('IDENT', recol_ident, None, 1))
                recol_ident = ''
                selector = ''
                

    # Imprimir tabla de símbolos
    print (str(tabla))
