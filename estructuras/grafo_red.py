# Grafo principal de la aplicación: ponderado, no dirigido y con listas de adyacencia.

from math import isfinite 
from servicios.auditoria import registrar_evento


class GrafoRed:

    # Qué hace: crea las listas vacías de servidores y sus conexiones.
    # Recibe: ningún dato adicional.
    # Devuelve: nada; inicializa el grafo. Cada conexión guarda (índice_vecino, latencia).
    def __init__(self):

        self.servidores = []
        self.adyacencias = []

    # Qué hace: verifica el nombre, audita y agrega un servidor sin conexiones.
    # Recibe: servidor, un objeto Servidor cuyo nombre debe ser único en la red.
    # Devuelve: un mensaje de confirmación (texto).
    # Lanza ValueError si el nombre ya existe u OSError si falla la auditoría.
    def agregar_servidor(self, servidor):
        for existente in self.servidores:
            if existente.nombre == servidor.nombre:
                raise ValueError(f"El servidor {servidor.nombre} ya existe en la red.")

        registrar_evento(
            "grafo_red",
            f"servidor {servidor.nombre} agregado a la red"
        )

        self.servidores.append(servidor)
        self.adyacencias.append([])
        return f"Servidor {servidor.nombre} agregado a la red."

    # Qué hace: valida, audita y agrega una conexión en ambos sentidos.
    # Recibe: nombre_origen y nombre_destino (textos), y latencia (número positivo y finito).
    # Devuelve: un mensaje de confirmación (texto).
    # Lanza ValueError por servidores inexistentes, autoenlaces, enlaces repetidos
    # o latencias inválidas; OSError si falla la auditoría.
    def agregar_conexion(self, nombre_origen, nombre_destino,latencia):
      origen = self.buscar_indice(nombre_origen)
      destino = self.buscar_indice(nombre_destino)

      if origen is None or destino is None:
            raise ValueError("Uno o ambos servidores no existen en la red.")

      if origen == destino:
            raise ValueError("No se puede crear una conexión entre el mismo servidor.")

      if not isfinite(latencia) or latencia <= 0:
            raise ValueError("La latencia debe ser un valor positivo y finito.")

      for vecino, peso in self.adyacencias[origen]:
            if vecino == destino:
                raise ValueError("La conexión ya existe.")

      registrar_evento(
          "grafo_red",
          f"conexión agregada entre {nombre_origen} y {nombre_destino} "
          f"con latencia {latencia} ms"
      )

      # Guardar ambas direcciones permite recorrer el enlace desde cualquiera de sus extremos.
      self.adyacencias[origen].append((destino, latencia))
      self.adyacencias[destino].append((origen, latencia))

      return f"Conexión agregada entre {nombre_origen} y {nombre_destino} con latencia {latencia}."


    # Qué hace: recorre la lista de servidores hasta encontrar el nombre solicitado.
    # Recibe: nombre (texto) del servidor que se busca.
    # Devuelve: su índice entero, incluido 0, o None si no existe. Costo: O(V).
    def buscar_indice(self, nombre):
        for indice in range (len(self.servidores)):
            if self.servidores[indice].nombre == nombre:
                return indice
        return None

    # Qué hace: audita y elimina la conexión en ambos sentidos, conservando los servidores.
    # Recibe: nombre_origen y nombre_destino (textos) de los extremos del enlace.
    # Devuelve: un mensaje de confirmación (texto).
    # Lanza ValueError si falta un servidor o el enlace; OSError si falla la auditoría.
    def eliminar_conexion(self, nombre_origen, nombre_destino):
        origen = self.buscar_indice(nombre_origen)
        destino = self.buscar_indice(nombre_destino)

        if origen is None or destino is None:
            raise ValueError("Uno o ambos servidores no existen en la red.")

        conexion_encontrada = None

        for conexion in self.adyacencias[origen]:
            if conexion[0] == destino:
                conexion_encontrada = conexion
                break

        if conexion_encontrada is None:
            raise ValueError("La conexión no existe.")

        registrar_evento(
            "grafo_red",
            f"conexión eliminada entre {nombre_origen} y {nombre_destino} "
            f"con latencia {conexion_encontrada[1]} ms"
        )

        self.adyacencias[origen].remove(conexion_encontrada)

        for conexion in self.adyacencias[destino]:
            if conexion[0] == origen:
                self.adyacencias[destino].remove(conexion)
                break

        return f"Conexión eliminada entre {nombre_origen} y {nombre_destino}."

    # Qué hace: recorre la red con BFS y detecta servidores inaccesibles o aislados.
    # Recibe: nombre_origen (texto) del servidor donde comienza el recorrido.
    # Devuelve: un diccionario con recorrido, no_alcanzables y aislados (listas de
    # nombres), y red_conectada (booleano). Lanza ValueError si el origen no existe.
    # Usa O(V + E) tiempo y O(V) memoria auxiliar; no modifica la red.
    def diagnosticar_red(self, nombre_origen):
        origen = self.buscar_indice(nombre_origen)

        if origen is None:
            raise ValueError("El servidor de origen no existe en la red.")

        visitados = [False] * len(self.servidores)
        cola = [origen]
        visitados[origen] = True
        recorrido = []

        # El índice avanza por la cola sin usar pop(0), evitando desplazar sus elementos.
        posicion = 0

        while posicion < len(cola):
            actual = cola[posicion]
            posicion += 1

            recorrido.append(self.servidores[actual].nombre)

            for vecino, latencia in self.adyacencias[actual]:
                if not visitados[vecino]:
                    # Se marca al encolar para evitar duplicados cuando hay ciclos.
                    visitados[vecino] = True
                    cola.append(vecino)

        # No alcanzable: no se visita desde el origen. Aislado: no tiene ninguna arista.
        # Un grupo separado puede ser no alcanzable sin contener servidores aislados.
        no_alcanzables = []
        aislados = []

        for indice in range(len(self.servidores)):
            if not visitados[indice]:
                no_alcanzables.append(self.servidores[indice].nombre)

            if len(self.adyacencias[indice]) == 0:
                aislados.append(self.servidores[indice].nombre)

        return {
            "recorrido": recorrido,
            "no_alcanzables": no_alcanzables,
            "aislados": aislados,
            "red_conectada": len(no_alcanzables) == 0
        }
        
