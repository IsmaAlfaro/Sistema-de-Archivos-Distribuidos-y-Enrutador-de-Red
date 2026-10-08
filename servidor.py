from nodo_archivo import NodoArchivo
from tabla_hash import TablaHash
from auditoria import registrar_evento


class Servidor:

    def __init__(self, nombre):  # Constructor
        self.nombre = nombre
        self.raiz = NodoArchivo("/", True)
        self.usuarios = TablaHash(nombre_servidor=nombre)

    def crear_nodo(self, nombre, es_carpeta, carpeta_padre="/"):
        if nombre.strip() == "" or "/" in nombre:
            return False

        padre = self.buscar_por_ruta(carpeta_padre)

        if padre is None or not padre.es_carpeta:
            return False

        if padre.buscar_hijo(nombre) is not None:
            return False

        if carpeta_padre == "/":
            ruta_nodo = f"/{nombre}"
        else:
            ruta_nodo = f"{carpeta_padre.rstrip('/')}/{nombre}"

        if es_carpeta:
            tipo_nodo = "carpeta"
        else:
            tipo_nodo = "archivo"

        registrar_evento(
            "servidor",
            f"creación de {tipo_nodo} '{ruta_nodo}' en {self.nombre}"
        )

        nuevo_nodo = NodoArchivo(nombre, es_carpeta)
        padre.agregar_hijo(nuevo_nodo)

        return True


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

        nodo_encontrado = padre.buscar_hijo(nombre)

        if nodo_encontrado is None:
            return False

        registrar_evento(
            "servidor",
            f"eliminación de nodo '{ruta}' en {self.nombre}"
        )

        return padre.eliminar(nombre)

    def mostrar_estructura(self):
         self.raiz.mostrar_arbol()
        
