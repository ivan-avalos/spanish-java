from enum import Enum
from tabla import LexToken, TablaLex, tokens
from arbol import Arbol, Nodo
from shared import Control
from pprint import pprint
from errors import Error

valores = ['IDENT', 'BOOLEAN_LIT', 'CHAR_LIT', 'INT_LIT', 'STRING_LIT']

operadores = [
    '>=', '<=', '==', '!=', '&&', '||', '++', '--',
    '=', '+', '-', '&', '|', '!', '<', '>'
]

class Selector(Enum):
    NINGUNO = 0
    DEF_VARIABLE = 1
    DIRECTIVA = 2
    EXPRESION = 3
    IF = 4
    FOR = 5
    WHILE = 6
    FUNCION = 7

class Parser:
    def __init__(self, input_file: str):
        self.arbol = Arbol()
        self.pila_selector = [
            [Selector.NINGUNO, []] # selector, recolector
        ]
        self.pila_arbol = [self.arbol.raiz]
        self.expresion = None
        self.tabla = TablaLex()
        self.tabla.importar(input_file + '.tab')
    
    def inicio (self):
        for t in self.tabla.tabla:
            r = self.procesar(t)
            if r == Control.ERROR: return 1
            while r != Control.SIGUIENTE:
                r = self.procesar(t)
                if r == Control.ERROR: return 1

        print(str(self.arbol))
        return 0

    def procesar (self, t: LexToken):
        if len(self.pila_selector) == 0:
            return Control.SIGUIENTE
            
        pprint (self.pila_selector[-1])
        
        cima = self.pila_selector[-1]
        
        if cima[0] == Selector.NINGUNO:
            # Entrada a definición de variable (o función)
            if t.tipo in ['BOOLEAN', 'CHAR', 'INT', 'VOID']:
                self.pila_selector.pop()
                self.pila_selector.append([Selector.DEF_VARIABLE, [t]])
                return Control.SIGUIENTE
            # Entrada a directiva del lenguaje
            elif t.tipo in ['PRINT', 'READ', 'RETURN']:
                self.pila_selector.pop()
                self.pila_selector.append([Selector.DIRECTIVA, [t]])
                return Control.SIGUIENTE
            # Entrada a expresión
            elif t.tipo in valores:
                self.pila_selector.pop()
                self.pila_selector.append([Selector.EXPRESION, [t]])
                return Control.SIGUIENTE
            # Entrada a if
            elif t.tipo == 'IF':
                self.pila_selector.pop()
                self.pila_selector.append([Selector.IF, []])
                return Control.SIGUIENTE
            # Entrada a for
            elif t.tipo == 'FOR':
                self.pila_selector.pop()
                self.pila_selector.append([Selector.FOR, []])
                return Control.SIGUIENTE
            # Entrada a while
            elif t.tipo == 'WHILE':
                self.pila_selector.pop()
                self.pila_selector.append([Selector.WHILE, []])
                return Control.SIGUIENTE

        if cima[0] == Selector.DEF_VARIABLE:
            return self.procesar_def_variable(t)

        if cima[0] == Selector.DIRECTIVA:
            return self.procesar_directiva(t)

        if cima[0] == Selector.EXPRESION:
            return self.procesar_expresion(t)

        if cima[0] == Selector.IF:
            return self.procesar_if(t)

        if cima[0] == Selector.FOR:
            return self.procesar_for(t)

        if cima[0] == Selector.WHILE:
            return self.procesar_while(t)

        if cima[0] == Selector.FUNCION:
            return self.procesar_funcion(t)

        return Control.SIGUIENTE

    def procesar_def_variable(self, t):
        recol = self.pila_selector[-1][1]
        
        # tipo
        if len(recol) == 1:
            if t.tipo != 'IDENT':
                Error('S_ESPERA_IDENT', t.numlinea)
                return Control.ERROR
            recol.append(t)
            return Control.SIGUIENTE
            
        # tipo + ident
        if len(recol) == 2:
            if t.tipo == ';':
                self.pila_arbol[-1].hijos.append(Nodo({
                    'selector': Selector.DEF_VARIABLE,
                    'tipo': recol[0].tipo,
                    'nombre': recol[1].nombre
                }))
                self.pila_selector.pop()
                self.pila_selector.append([Selector.NINGUNO, []])
            elif t.tipo == '=':
                recol.append(t)
            else:
                Error('S_ESPERA_PC_O_IGUAL', t.numlinea)
                return Control.ERROR
            return Control.SIGUIENTE

        # tipo + ident + =
        if len(recol) == 3:
            if t.tipo in valores:
                self.pila_selector.append([Selector.EXPRESION, [t]])
                recol.append(t)
            else:
                Error('S_ESPERA_EXPR', t.numlinea)
                return Control.ERROR
            return Control.SIGUIENTE

        # tipo + ident + = + expr
        if len(recol) == 4:
            if t.tipo == ';':
                self.pila_arbol[-1].hijos.append(Nodo({
                    'selector': Selector.DEF_VARIABLE,
                    'tipo': recol[0].tipo,
                    'nombre': recol[1].nombre,
                    'valor': self.expresion
                }))
                self.expresion = None
                self.pila_selector.pop()
                self.pila_selector.append([Selector.NINGUNO, []])
            else:
                Error('S_ESPERA_PC', t.numlinea)
                return Control.ERROR

        return Control.SIGUIENTE

    def procesar_directiva(self, t):
        recol = self.pila_selector[-1][1]
        
        # directiva
        if len(recol) == 1:
            if t.tipo in valores:
                self.pila_selector.append([Selector.EXPRESION, [t]])
                recol.append(t)
            else:
                Error('S_ESPERA_EXPR', t.numlinea)
                return Control.ERROR
            return Control.SIGUIENTE

        # directiva + expr
        if len(recol) == 2:
            if t.tipo == ';':
                self.pila_arbol[-1].hijos.append(Nodo({
                    'selector': Selector.DIRECTIVA,
                    'expresion': self.expresion
                }))
                self.expresion = None
                self.pila_selector.pop()
                self.pila_selector.append([Selector.NINGUNO, []])
            else:
                Error('S_ESPERA_EXPR', t.numlinea)
                return Control.ERROR

        return Control.SIGUIENTE

    def procesar_expresion(self, t):
        recol = self.pila_selector[-1][1]
        tipo_ultimo = recol[-1].tipo

        if len(recol) == 1:
            if tipo_ultimo in valores:
                recol.append(recol[-1])
            else:
                Error('S_ESPERA_IDENT_O_LIT', t.numlinea)
                return Control.ERROR
            
        if tipo_ultimo in valores and t.tipo in operadores:
            recol.append(t)  
        elif tipo_ultimo in operadores and t.tipo in valores:
            recol.append(t)
        elif tipo_ultimo in valores and t.tipo in valores:
            Error('S_ESPERA_OPER', t.numlinea)
            return Control.ERROR
        elif tipo_ultimo in operadores and t.tipo in operadores:
            Error('S_ESPERA_IDENT_O_LIT', t.numlinea)
            return Control.ERROR
        else:
            self.expresion = recol[1:]
            self.pila_selector.pop()
            return Control.REPETIR

        return Control.SIGUIENTE

    def procesar_if(self, t):
        return

    def procesar_for(self, t):
        return

    def procesar_while(self, t):
        return

    def procesar_funcion(self, t):
        return
