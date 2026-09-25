from nodo_archivo import NodoArchivo


class Servidor:

    def __init__(self, nombre):  # Constructor
        self.nombre = nombre
        self.raiz = NodoArchivo("/", True)
        
        
    def crear_nodo(self, nombre, es_carpeta, carpeta_padre="/"):
        nuevo_nodo = NodoArchivo(nombre, es_carpeta)

        if carpeta_padre == "/":
            self.raiz.agregar_hijo(nuevo_nodo)
            return True
        
        padre = self.raiz.buscar(carpeta_padre)
        
        if padre is not None and padre.es_carpeta:
            padre.agregar_hijo(nuevo_nodo)
            return True
        
        return False 
    
              
    def buscar_nodo(self, nombre):
         return self.raiz.buscar(nombre)
       
     
    def eliminar_nodo(self, nombre):
         return self.raiz.eliminar(nombre)
     
    def mostrar_estructura(self):
         self.raiz.mostrar_arbol()