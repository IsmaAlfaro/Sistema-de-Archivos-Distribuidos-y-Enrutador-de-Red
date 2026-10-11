# Nodo del árbol general de archivos: una carpeta admite hijos y un archivo es hoja.
class NodoArchivo:
    
    # Qué hace: crea un nodo con una lista de hijos vacía.
    # Recibe: nombre (texto) y es_carpeta (True para carpeta, False para archivo).
    # Devuelve: nada; inicializa los datos del objeto.
    def __init__(self, nombre, es_carpeta):
        self.nombre = nombre
        self.es_carpeta = es_carpeta
        self.hijos = []
        
        
    # Qué hace: agrega un hijo si el nodo actual es una carpeta; en archivos no lo agrega.
    # Recibe: hijo, un objeto NodoArchivo.
    # Devuelve: nada.
    def agregar_hijo(self, hijo):
        if self.es_carpeta:
            self.hijos.append(hijo)
            
            
    # Qué hace: busca un nombre únicamente entre los hijos directos del nodo.
    # Recibe: nombre (texto) del archivo o carpeta que se quiere localizar.
    # Devuelve: el primer NodoArchivo coincidente o None si no existe.
    def buscar_hijo(self, nombre):
        for hijo in self.hijos:
            if hijo.nombre == nombre:
                return hijo

        return None 

        
    # Qué hace: busca recursivamente en este nodo y en todos sus descendientes.
    # Recibe: nombre (texto) del archivo o carpeta que se quiere localizar.
    # Devuelve: el primer NodoArchivo coincidente o None si no existe.
    def buscar(self, nombre):
        if self.nombre == nombre:
            return self

        for hijo in self.hijos:
            encontrado = hijo.buscar(nombre)

            if encontrado is not None:  # Propaga el nodo hallado hacia quien inició la búsqueda.
                return encontrado

        return None
    
    
    # Qué hace: muestra este nodo y sus descendientes con sangría según su nivel.
    # Recibe: nivel (entero, 0 por defecto), usado para calcular la sangría.
    # Devuelve: nada; imprime el árbol en consola.
    def mostrar_arbol(self, nivel=0):
        print("  " * nivel + self.nombre)

        for hijo in self.hijos:
            hijo.mostrar_arbol(nivel + 1)
         
            
    # Qué hace: vacía recursivamente los descendientes y limpia la lista de hijos.
    # Recibe: ningún dato adicional; utiliza los hijos del nodo actual.
    # Devuelve: nada; el nodo actual permanece en su padre.
    # Python libera los nodos cuando ya no quedan referencias a ellos.
    def eliminar_contenido(self):
        for hijo in self.hijos:
            hijo.eliminar_contenido()
    
        self.hijos.clear()
           
            
    # Qué hace: vacía un hijo directo y sus descendientes, y lo retira de la lista.
    # Recibe: nombre (texto) del hijo que se quiere eliminar.
    # Devuelve: True si lo elimina o False si no encuentra ese hijo.
    def eliminar(self, nombre):
        for hijo in self.hijos:
            if hijo.nombre == nombre:
                hijo.eliminar_contenido()
                self.hijos.remove(hijo)
                return True

        return False
