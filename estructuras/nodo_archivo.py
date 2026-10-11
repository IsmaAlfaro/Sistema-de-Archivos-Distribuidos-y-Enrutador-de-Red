# Nodo del árbol general de archivos: una carpeta admite hijos y un archivo es hoja.
class NodoArchivo:
    
    # Recibe el nombre y un booleano de tipo; inicia una lista de hijos vacía.
    def __init__(self, nombre, es_carpeta):
        self.nombre = nombre
        self.es_carpeta = es_carpeta
        self.hijos = []
        
        
    # Recibe otro NodoArchivo y lo agrega solo si este nodo es una carpeta.
    # No devuelve un resultado; en archivos no realiza ninguna modificación.
    def agregar_hijo(self, hijo):
        if self.es_carpeta:
            self.hijos.append(hijo)
            
            
    # Busca únicamente entre hijos directos y devuelve el nodo coincidente o None.
    # Se usa para resolver un nivel de una ruta y detectar nombres repetidos.
    def buscar_hijo(self, nombre):
        for hijo in self.hijos:
            if hijo.nombre == nombre:
                return hijo

        return None 

        
    # Búsqueda recursiva en profundidad: revisa este nodo y luego sus descendientes.
    # Devuelve la primera coincidencia por nombre o None si no encuentra ninguna.
    def buscar(self, nombre):
        if self.nombre == nombre:
            return self

        for hijo in self.hijos:
            encontrado = hijo.buscar(nombre)

            if encontrado is not None:  # Propaga el nodo hallado hacia quien inició la búsqueda.
                return encontrado

        return None
    
    
    # Imprime este nodo y su subárbol con dos espacios por nivel; no devuelve datos.
    # Cada llamada recursiva incrementa el nivel para representar la jerarquía.
    def mostrar_arbol(self, nivel=0):
        print("  " * nivel + self.nombre)

        for hijo in self.hijos:
            hijo.mostrar_arbol(nivel + 1)
         
            
    # Vacía recursivamente los hijos antes de limpiar la lista de este nodo (postorden).
    # No elimina este nodo de su padre ni devuelve datos. Python recupera los objetos
    # cuando dejan de existir referencias a ellos, incluidas las referencias externas.
    def eliminar_contenido(self):
        for hijo in self.hijos:
            hijo.eliminar_contenido()
    
        self.hijos.clear()
           
            
     # Elimina únicamente un hijo directo con el nombre recibido.
    # Vacía su contenido recursivamente antes de retirarlo de esta carpeta.
    # Devuelve True si lo elimina o False si no existe entre los hijos directos.
    def eliminar(self, nombre):
        for hijo in self.hijos:
            if hijo.nombre == nombre:
                hijo.eliminar_contenido()
                self.hijos.remove(hijo)
                return True

        return False
