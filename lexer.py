from enum import Enum
from symbol import LexToken, TablaLex, tokens

def inicio_lexer(data):
    tabla = TablaLex()
    
    selector = ''
    recol_string = ''
    recol_caracter = ''
    recol_comentario = ''
    recol_operador = ''
    
    for c in data + "\n":
        print (c + ' (' + selector + ')')
        
        if selector == '':
            # Entradas a tokens
            if c == '"':
                selector = 'STRING_LIT'
                continue
            elif c == '\'':
                selector = 'CHAR_LIT'
                continue
            elif c == '/':
                recol_comentario = '/'
            elif (c == '=' or c == '+' or c == '-' or c == '&' or c == '|') and len(recol_operador) == 0:
                recol_operador = c
                continue
            elif c == '!' or c == '<' or c == '>':
                recol_operador = c
                continue
            elif c == '{':
                tabla.insertar(LexToken('{', None, None, 1))
            elif c == '}':
                tabla.insertar(LexToken('}', None, None, 1))
            elif c == '(':
                tabla.insertar(LexToken('(', None, None, 1))
            elif c == ')':
                tabla.insertar(LexToken(')', None, None, 1))
            elif c == ',':
                tabla.insertar(LexToken(',', None, None, 1))
            elif c == ';':
                tabla.insertar(LexToken(';', None, None, 1))
            elif c == '*':
                tabla.insertar(LexToken('*', None, None, 1))

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
            continue

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
                continue
            else:
                recol_caracter += c

        # Comentarios
        if selector == 'COMMENT':
            if c == '*':
                recol_comentario = c
                continue
            elif recol_comentario == '*':
                if c == '/':
                    selector = ''
                    recol_comentario = ''
                    continue
                else:
                    recol_comentario = ''
                    continue

    # Imprimir tabla de símbolos
    print (str(tabla))
