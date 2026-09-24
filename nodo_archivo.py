class NodoArchivo:
    def __init__(self, nombre, es_carpeta):#constructor
        self.nombre = nombre
        self.es_carpeta = es_carpeta
        self.hijos = []
