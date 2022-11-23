import uuid, json
import graphviz as gv
from pprint import pformat

class Nodo:
    def __init__(self, dato = None):
        self.dato = dato
        self.hijos = []

    def print(self, n = 0):
        s = '  ' * n + 'Nodo:' + "\n"
        s += '  ' * n + "dato = " + str(self.dato) + "\n"
        s += '  ' * n + "hijos =\n"
        for h in self.hijos:
            s += h.print(n + 1)
        s += "\n"
        return s

    def render(self, dot: gv.Digraph, parent: str):
        name = uuid.uuid1().hex
        fdato = pformat(self.dato, indent=2).replace('\n', '\l')
        dot.node(name, fdato)
        if parent:
            dot.edge(parent, name)
        
        for h in self.hijos:
            h.render(dot, name)

    def __str__(self):
        return self.print()


class Arbol:
    def __init__(self, raiz: Nodo = Nodo()):
        self.raiz = raiz

    def render(self, filename, view = False):
        dot = gv.Digraph()
        dot.attr(rankdir='LR')
        dot.attr('node', fontname='monospace')
        self.raiz.render(dot, None)
        dot.render(filename, view = view)

    def __str__(self):
        if self.raiz:
            return str(self.raiz)
        return "None"
