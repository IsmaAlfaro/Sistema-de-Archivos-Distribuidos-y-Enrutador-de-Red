from nodo_archivo import NodoArchivo


class Servidor:

    def __init__(self, nombre):  # Constructor
        self.nombre = nombre
        self.raiz = NodoArchivo("/", True)