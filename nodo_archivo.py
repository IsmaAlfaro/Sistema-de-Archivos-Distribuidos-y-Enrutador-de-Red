class NodoArchivo:
    def __init__(self, nombre, es_carpeta):#constructor
        self.nombre = nombre
        self.es_carpeta = es_carpeta
        self.hijos = []
        
    def agregar_hijo(self, hijo):#permite agregar un hijo a la lista de hijos del nodo
        if self.es_carpeta:
            self.hijos.append(hijo)