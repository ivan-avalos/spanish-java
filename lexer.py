from enum import Enum
from symbol import LexToken, TablaLex, tokens

t_boolean = 'booleano'
t_break = 'detener'
t_char = 'caracter'
t_double = 'doble'
t_else = 'si no'
t_for = 'por cada'
t_ident = r'[a-zA-Z_][a-zA-Z0-9_]?'
t_if = 'si'
t_int = 'entero'
t_print = 'imprimir'
t_read = 'leer'
t_return = 'retorna'
t_string = 'cadena'
t_void = 'vacio'
t_while = 'mientras'

t_boolean_lit = r'verdadero|falso'
t_char_lit = r'\'[[:print:]]\''
t_double_lit = r'\d+.\d+'
t_int_lit = r'\d+'
t_string_lit = r'"[[:print]]*"'

def inicio_lexer(data):
    tabla = TablaLex()
    
    es_string = False
    es_caracter = False
    es_comentario = False
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

    print (str(tabla))
        
    '''
    tabla = TablaLex()
    # booleano ivan = verdadero
    tabla.insertar(LexToken('BOOLEAN', None, None, 1))
    tabla.insertar(LexToken('IDENT', 'ivan', None, 1))
    tabla.insertar(LexToken('=', None, None, 1))
    tabla.insertar(LexToken('BOOLEAN_LIT', None, True, 1))
    print (str(tabla))

    ident = tabla.buscar('ivan')
    print (str(ident))
    
    ident.valor = True
    tabla.actualizar('ivan', ident)
    ident = tabla.buscar('ivan')
    print (str(ident))
    '''
