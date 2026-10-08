# Agrupa el árbol de directorios y las credenciales independientes de un servidor.
from nodo_archivo import NodoArchivo
from tabla_hash import TablaHash
from auditoria import registrar_evento


class Servidor:

    # Recibe el nombre, crea la raíz / y una tabla hash asociada a este servidor.
    def __init__(self, nombre):
        self.nombre = nombre
        self.raiz = NodoArchivo("/", True)
        self.usuarios = TablaHash(nombre_servidor=nombre)

    # Crea un archivo o carpeta dentro de la ruta indicada (por defecto, la raíz).
    # Devuelve False si el padre no es una carpeta válida o el nombre ya está en ella.
    # Audita antes de insertar y devuelve True al completar la creación.
    # Un fallo de escritura de auditoría se propaga al código que llama al método.
    def crear_nodo(self, nombre, es_carpeta, carpeta_padre="/"):
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


    # Busca recursivamente desde la raíz y devuelve el primer nodo con ese nombre o None.
    def buscar_nodo(self, nombre):
         return self.raiz.buscar(nombre)

    # Separa una ruta por / y resuelve cada componente entre los hijos directos.
    # Devuelve la raíz para /, el nodo encontrado o None si falta algún componente.
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


    # Obtiene el padre de la ruta, verifica una coincidencia y audita la eliminación.
    # Rechaza la raíz; devuelve False si no encuentra padre/nodo y el resultado de
    # padre.eliminar en caso contrario. Los errores de auditoría se propagan.
    # Pendiente: la búsqueda por nombre recorre descendientes y puede afectar otra ruta.
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

    # Imprime desde la raíz toda la jerarquía del servidor; no devuelve datos.
    def mostrar_estructura(self):
         self.raiz.mostrar_arbol()
        
