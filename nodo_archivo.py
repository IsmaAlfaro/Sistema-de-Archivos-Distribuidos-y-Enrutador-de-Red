class NodoArchivo:
    
    def __init__(self, nombre, es_carpeta):#constructor
        self.nombre = nombre
        self.es_carpeta = es_carpeta
        self.hijos = []
        
        
    def agregar_hijo(self, hijo):#permite agregar un hijo a la lista de hijos del nodo
        if self.es_carpeta:
            self.hijos.append(hijo)
            
            
    def buscar_hijo(self, nombre):
        for hijo in self.hijos:
            if hijo.nombre == nombre:
                return hijo

        return None 

        
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
         
            
    def eliminar_contenido(self):#vacia el contenido de un nodo y sus hijos de manera recursiva
        for hijo in self.hijos:
            hijo.eliminar_contenido()
    
        self.hijos.clear()
           
            
    def eliminar(self, nombre): #busca lo que voy a eliminar
        for hijo in self.hijos:
            if hijo.nombre == nombre:
                hijo.eliminar_contenido()
                self.hijos.remove(hijo)
                return True

            if hijo.eliminar(nombre):
                return True

        return False
    
   