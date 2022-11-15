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

    def __str__(self):
        return self.print()


class Arbol:
    def __init__(self, raiz: Nodo = Nodo()):
        self.raiz = raiz

    def __str__(self):
        if self.raiz:
            return str(self.raiz)
        return "None"
