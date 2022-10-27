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
