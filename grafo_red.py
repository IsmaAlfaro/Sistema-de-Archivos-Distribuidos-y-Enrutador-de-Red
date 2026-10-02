class GrafoRed: 

    def __init__(self):

        self.servidores = []
        self.adyacencias = []

    def agregar_servidor(self, servidor):
        for existente in self.servidores:
            if existente.nombre == servidor.nombre:
                raise ValueError(f"El servidor {servidor.nombre} ya existe en la red.")

        self.servidores.append(servidor)
        self.adyacencias.append([])
        return f"Servidor {servidor.nombre} agregado a la red."

    def agregar_conexion(self, nombre_origen, nombre_destino,latencia):
      origen = self.buscar_indice(nombre_origen)
      destino = self.buscar_indice(nombre_destino)

      if origen is None or destino is None:
            raise ValueError("Uno o ambos servidores no existen en la red.")

      if origen == destino:
            raise ValueError("No se puede crear una conexión entre el mismo servidor.")

      if latencia <= 0:
            raise ValueError("La latencia debe ser un valor positivo.")

      for vecino, peso in self.adyacencias[origen]:
            if vecino == destino:
                raise ValueError("La conexión ya existe.")

      self.adyacencias[origen].append((destino, latencia))
      self.adyacencias[destino].append((origen, latencia))
      
      return f"Conexión agregada entre {nombre_origen} y {nombre_destino} con latencia {latencia}."
      
    def buscar_indice(self, nombre):
        for indice in range (len(self.servidores)):
            if self.servidores[indice].nombre == nombre:
                return indice
        return None

    def eliminar_conexion(self, nombre_origen, nombre_destino):
        origen = self.buscar_indice(nombre_origen)
        destino = self.buscar_indice(nombre_destino)

        if origen is None or destino is None:
            raise ValueError("Uno o ambos servidores no existen en la red.")

        for conexion in self.adyacencias[origen]:
            if conexion[0] == destino:
                self.adyacencias[origen].remove(conexion)
                break

        else:
            raise ValueError("La conexión no existe.")

        for conexion in self.adyacencias[destino]:
            if conexion[0] == origen:
                self.adyacencias[destino].remove(conexion)
                break

        return f"Conexión eliminada entre {nombre_origen} y {nombre_destino}."

    def diagnosticar_red(self, nombre_origen):
        origen = self.buscar_indice(nombre_origen)

        if origen is None:
            raise ValueError("El servidor de origen no existe en la red.")

        visitados = [False] * len(self.servidores)
        cola = [origen]
        visitados[origen] = True
        recorrido = []

        posicion = 0

        while posicion < len(cola):
            actual = cola[posicion]
            posicion += 1

            recorrido.append(self.servidores[actual].nombre)

            for vecino, latencia in self.adyacencias[actual]:
                if not visitados[vecino]:
                    visitados[vecino] = True
                    cola.append(vecino)

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