# Agrupa el árbol de directorios y las credenciales independientes de un servidor.
from estructuras.nodo_archivo import NodoArchivo
from estructuras.tabla_hash import TablaHash
from servicios.auditoria import registrar_evento


class Servidor:

    # Qué hace: crea un servidor con una carpeta raíz / y su tabla de usuarios.
    # Recibe: nombre (texto) que identifica al servidor.
    # Devuelve: nada; inicializa los datos del objeto.
    def __init__(self, nombre):
        self.nombre = nombre
        self.raiz = NodoArchivo("/", True)
        self.usuarios = TablaHash(nombre_servidor=nombre)

    # Qué hace: valida, registra en auditoría y crea un archivo o una carpeta.
    # Recibe: nombre (texto), es_carpeta (booleano) y carpeta_padre (ruta, / por defecto).
    # Devuelve: True si crea el nodo; False si el nombre es inválido, está repetido
    # en esa carpeta o la ruta de destino no corresponde a una carpeta existente.
    # Si falla la auditoría, lanza OSError antes de insertar el nodo.
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


    # Qué hace: busca recursivamente un archivo o carpeta desde la raíz.
    # Recibe: nombre (texto) del nodo que se quiere encontrar.
    # Devuelve: el primer NodoArchivo coincidente o None si no existe.
    def buscar_nodo(self, nombre):
         return self.raiz.buscar(nombre)

    # Qué hace: recorre los componentes de una ruta para localizar su nodo exacto.
    # Recibe: ruta (texto), por ejemplo /Documentos/Tareas; / representa la raíz.
    # Devuelve: el NodoArchivo encontrado o None si algún componente no existe.
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


    # Qué hace: localiza el nodo por su ruta, audita y lo elimina con sus descendientes.
    # Recibe: ruta (texto) del archivo o carpeta que se quiere eliminar.
    # Devuelve: True si lo elimina; False si no existe o se intenta eliminar la raíz.
    # Si falla la auditoría, lanza OSError antes de borrar el nodo.
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

    # Qué hace: muestra todo el árbol de archivos y carpetas del servidor.
    # Recibe: ningún dato adicional; utiliza la raíz del servidor actual.
    # Devuelve: nada; imprime la estructura en consola.
    def mostrar_estructura(self):
         self.raiz.mostrar_arbol()
        
