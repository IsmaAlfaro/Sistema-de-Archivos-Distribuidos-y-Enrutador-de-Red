# Grafo principal de la aplicación: ponderado, no dirigido y con listas de adyacencia.

from math import isfinite 
from servicios.auditoria import registrar_evento


class GrafoRed:

    # Inicia listas paralelas: servidores[i] identifica al dueño de adyacencias[i].
    # Cada entrada de vecinos será una tupla (indice_vecino, latencia).
    def __init__(self):

        self.servidores = []
        self.adyacencias = []

    # Recibe un objeto Servidor, verifica nombre único y crea su lista de vecinos.
    # Devuelve un mensaje de éxito; lanza ValueError si el nombre ya está registrado.
    # Audita antes de modificar la red y propaga fallos de escritura del log.
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

    # Recibe dos nombres existentes y una latencia numérica; agrega el enlace en ambos lados.
    # Rechaza servidores inexistentes, autoenlaces, duplicados y latencias <= 0 con ValueError.
    # Audita antes de insertar y devuelve un mensaje
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


    # Busca un nombre secuencialmente en O(V) y devuelve su índice o None.
    # El índice 0 es válido; quien llama debe distinguirlo de None.
    def buscar_indice(self, nombre):
        for indice in range (len(self.servidores)):
            if self.servidores[indice].nombre == nombre:
                return indice
        return None

    # Localiza y elimina un enlace en ambos sentidos, conservando los servidores.
    # Devuelve un mensaje o lanza ValueError si falta un servidor o la conexión.
    # Registra el evento antes del borrado; un error de auditoría se propaga.
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

    # Ejecuta BFS desde el nombre recibido; lanza ValueError si no existe el origen.
    # Devuelve un diccionario con recorrido, no_alcanzables, aislados y red_conectada.
    # Usa O(V + E) tiempo en el peor caso y O(V) memoria auxiliar; no cambia la red.
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
        
