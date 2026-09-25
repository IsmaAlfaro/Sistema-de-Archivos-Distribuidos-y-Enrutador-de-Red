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

        padre = self.buscar_por_ruta(carpeta_padre)

        if padre is not None and padre.es_carpeta:
            padre.agregar_hijo(nuevo_nodo)
            return True

        return False
    
              
    def buscar_nodo(self, nombre):
         return self.raiz.buscar(nombre)
     
    def buscar_por_ruta(self, ruta):
        if ruta == "/":
            return self.raiz

        partes = ruta.strip("/").split("/")
        nodo_actual = self.raiz

        for parte in partes:
            nodo_actual = nodo_actual.buscar_hijo(parte)

            if nodo_actual is None:
                return None

        return nodo_actual
            
        
    def eliminar_nodo(self, ruta):
        if ruta == "/":
            return False

        partes = ruta.strip("/").split("/")
        nombre = partes[-1]

        ruta_padre = "/" + "/".join(partes[:-1])

        padre = self.buscar_por_ruta(ruta_padre)

        if padre is None:
            return False

        return padre.eliminar(nombre)
     
    def mostrar_estructura(self):
         self.raiz.mostrar_arbol()
         
    