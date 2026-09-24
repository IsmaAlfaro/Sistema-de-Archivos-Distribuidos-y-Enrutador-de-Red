class NodoArchivo:
    def __init__(self, nombre, es_carpeta):#constructor
        self.nombre = nombre
        self.es_carpeta = es_carpeta
        self.hijos = []
        
    def agregar_hijo(self, hijo):#permite agregar un hijo a la lista de hijos del nodo
        if self.es_carpeta:
            self.hijos.append(hijo)

        
    def buscar(self, nombre):#busca de manera recursiva un nodo con el nombre especificado en el árbol de nodos
        if self.nombre == nombre:
            return self

        for hijo in self.hijos:
            encontrado = hijo.buscar(nombre)

            if encontrado is not None:#si encontro algo devuelvelo.
                return encontrado

        return None
    
    def mostrar_arbol(self, nivel=0):
        print("  " * nivel + self.nombre)

        for hijo in self.hijos:
            hijo.mostrar_arbol(nivel + 1)