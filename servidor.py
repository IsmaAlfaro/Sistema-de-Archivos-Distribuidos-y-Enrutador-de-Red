from nodo_archivo import NodoArchivo


class Servidor:

    def __init__(self, nombre):  # Constructor
        self.nombre = nombre
        self.raiz = NodoArchivo("/", True)
        
        
    def crear_nodo(self, nombre, es_carpeta):
        nuevo_nodo = NodoArchivo(nombre, es_carpeta)
        self.raiz.agregar_hijo(nuevo_nodo)
        
        
    def buscar_nodo(self, nombre):
         return self.raiz.buscar(nombre)
     
     
    def eliminar_nodo(self, nombre):
         return self.raiz.eliminar(nombre)
     
    def mostrar_estructura(self):
         self.raiz.mostrar_arbol()