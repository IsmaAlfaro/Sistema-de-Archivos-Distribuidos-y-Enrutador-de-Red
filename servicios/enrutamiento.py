# enrutamiento.py
# Módulo de enrutamiento: calcula la ruta de menor latencia entre servidores
# usando el algoritmo de Dijkstra sobre el GrafoRed que ya existe.
#
# Idea general:
#   - El grafo guarda los servidores en red.servidores y sus conexiones en
#     red.adyacencias[i] = [(indice_vecino, latencia), ...].
#   - Dijkstra trabaja con ÍNDICES. Los nombres solo se usan al recibir
#     datos del usuario y al mostrar resultados.

from servicios.auditoria import registrar_evento


# Representa "todavía no se conoce ningún camino hasta este servidor".
# Es mayor que cualquier número, así que cualquier latencia real lo mejora.
INFINITO = float("inf")


# Qué hace: busca el servidor no visitado con la menor distancia finita en O(V).
# Recibe: distancias (lista de costos) y visitados (lista de booleanos), del mismo tamaño.
# Devuelve: el índice del servidor elegido o None si no quedan candidatos alcanzables.
def buscar_minimo_no_visitado(distancias, visitados):
    """
    Devuelve el índice del servidor NO visitado con menor distancia.
    Devuelve None si no queda ninguno alcanzable (todos visitados o en INFINITO).
    """
    mejor_indice = None
    mejor_distancia = INFINITO

    for indice in range(len(distancias)):
        # La comparación es estricta (<): un servidor en INFINITO nunca se elige.
        if not visitados[indice] and distancias[indice] < mejor_distancia:
            mejor_distancia = distancias[indice]
            mejor_indice = indice

    return mejor_indice


# Qué hace: calcula con Dijkstra el costo mínimo del origen a cada servidor.
# Recibe: red (GrafoRed con pesos no negativos) e indice_origen (índice entero válido).
# Devuelve: dos listas, distancias y predecesores; los destinos inaccesibles quedan
# con distancia infinita. No modifica la red ni registra eventos de auditoría.
# Costo: O(V² + E) tiempo y O(V) memoria auxiliar.
def dijkstra(red, indice_origen):
    """
    Calcula la menor latencia desde indice_origen hacia todos los servidores.

    Recibe:
        red: el GrafoRed ya existente (no se crea otro grafo).
        indice_origen: posición del servidor de origen en red.servidores.

    Devuelve (distancias, predecesores):
        distancias[i]   = menor latencia desde el origen hasta i (INFINITO si no hay ruta).
        predecesores[i] = índice del servidor anterior a i en el mejor camino
                          (None si es el origen o no se llegó a él).
    """
    cantidad = len(red.servidores)

    distancias = [INFINITO] * cantidad     # mejor costo conocido hasta cada servidor
    visitados = [False] * cantidad         # True = distancia ya definitiva
    predecesores = [None] * cantidad       # de dónde se llegó a cada servidor

    # El origen está a latencia 0 de sí mismo.
    distancias[indice_origen] = 0

    while True:
        # 1. Elegir el servidor no visitado con menor distancia.
        actual = buscar_minimo_no_visitado(distancias, visitados)

        # Si no queda ninguno alcanzable, el algoritmo terminó.
        if actual is None:
            break

        # 2. Su distancia ya es definitiva (las latencias son positivas).
        visitados[actual] = True

        # 3. Relajación: ¿llegar al vecino pasando por "actual" es más barato?
        for vecino, latencia in red.adyacencias[actual]:
            if visitados[vecino]:
                continue

            nueva_distancia = distancias[actual] + latencia

            if nueva_distancia < distancias[vecino]:
                distancias[vecino] = nueva_distancia
                predecesores[vecino] = actual

    return distancias, predecesores


# Qué hace: sigue los predecesores hacia atrás e invierte el recorrido para formar la ruta.
# Recibe: predecesores (lista generada por Dijkstra) e indice_destino (entero válido
# de un destino alcanzable).
# Devuelve: una lista nueva de índices ordenados desde el origen hasta el destino.
def reconstruir_ruta(predecesores, indice_destino):
    """
    Reconstruye la ruta como lista de índices, desde el origen hasta el destino.

    Se parte del destino y se retrocede con los predecesores hasta llegar al
    origen (cuyo predecesor es None). Como así queda al revés, se invierte.
    Solo debe llamarse si el destino es alcanzable.
    """
    ruta = []
    actual = indice_destino

    while actual is not None:
        ruta.append(actual)
        actual = predecesores[actual]

    ruta.reverse()
    return ruta


# Qué hace: busca la latencia de una conexión directa entre dos servidores.
# Recibe: red (GrafoRed), indice_a e indice_b (índices enteros válidos).
# Devuelve: la latencia numérica del enlace o None si no están conectados directamente.
def buscar_latencia(red, indice_a, indice_b):
    """Devuelve la latencia de la conexión directa entre dos servidores."""
    for vecino, latencia in red.adyacencias[indice_a]:
        if vecino == indice_b:
            return latencia
    return None


# Qué hace: valida los servidores, calcula la ruta de menor latencia y audita el resultado.
# Recibe: red (GrafoRed), nombre_origen y nombre_destino (textos).
# Devuelve: un diccionario con hay_ruta (booleano), ruta (lista de nombres),
# latencias_por_salto (lista de números) y latencia_total (número o None si no hay ruta).
# Lanza ValueError si falta un servidor y OSError si falla la auditoría.
def calcular_ruta(red, nombre_origen, nombre_destino):
    """
    Calcula la ruta de menor latencia entre dos servidores, dados por nombre.

    Lanza ValueError si el origen o el destino no existen (igual que GrafoRed).
    Devuelve un diccionario:
        "hay_ruta":            True/False
        "ruta":                lista de nombres de servidores en orden
        "latencias_por_salto": latencia de cada salto
        "latencia_total":      suma de latencias (None si no hay ruta)
    """
    indice_origen = red.buscar_indice(nombre_origen)
    indice_destino = red.buscar_indice(nombre_destino)

    if indice_origen is None:
        raise ValueError("El servidor de origen no existe en la red.")

    if indice_destino is None:
        raise ValueError("El servidor de destino no existe en la red.")

    # Caso especial: no hace falta viajar.
    if indice_origen == indice_destino:
        resultado = {
            "hay_ruta": True,
            "ruta": [nombre_origen],
            "latencias_por_salto": [],
            "latencia_total": 0
        }

        registrar_evento(
            "enrutamiento",
            f"cálculo de ruta de {nombre_origen} a {nombre_destino}: "
            f"{nombre_origen}, latencia total 0 ms"
        )

        return resultado

    distancias, predecesores = dijkstra(red, indice_origen)

    # Si la distancia sigue en INFINITO, ningún camino llegó al destino.
    if distancias[indice_destino] == INFINITO:
        resultado = {
            "hay_ruta": False,
            "ruta": [],
            "latencias_por_salto": [],
            "latencia_total": None
        }

        registrar_evento(
            "enrutamiento",
            f"cálculo de ruta de {nombre_origen} a {nombre_destino}: "
            "no hay ruta disponible"
        )

        return resultado

    indices_ruta = reconstruir_ruta(predecesores, indice_destino)

    nombres = []
    for indice in indices_ruta:
        nombres.append(red.servidores[indice].nombre)

    latencias_por_salto = []
    for posicion in range(1, len(indices_ruta)):
        anterior = indices_ruta[posicion - 1]
        siguiente = indices_ruta[posicion]
        latencias_por_salto.append(buscar_latencia(red, anterior, siguiente))

    resultado = {
        "hay_ruta": True,
        "ruta": nombres,
        "latencias_por_salto": latencias_por_salto,
        "latencia_total": distancias[indice_destino]
    }

    registrar_evento(
        "enrutamiento",
        f"cálculo de ruta de {nombre_origen} a {nombre_destino}: "
        f"{' -> '.join(nombres)}, latencia total "
        f"{distancias[indice_destino]} ms"
    )

    return resultado


# Qué hace: muestra la ruta, los saltos y el costo de un envío simulado entre servidores.
# Recibe: red (GrafoRed), nombre_origen y nombre_destino (textos).
# Devuelve: el diccionario de calcular_ruta y propaga sus errores.
# Es una simulación: no transmite datos por una red física ni mueve archivos.
def simular_envio_paquete(red, nombre_origen, nombre_destino):
    """
    Simula el envío de un paquete mostrando cada salto y la latencia total.
    Lanza ValueError si el origen o el destino no existen.
    Devuelve el mismo diccionario de calcular_ruta.
    """
    resultado = calcular_ruta(red, nombre_origen, nombre_destino)

    print(f"\nEnviando paquete de {nombre_origen} a {nombre_destino}...")

    if not resultado["hay_ruta"]:
        print("No existe una ruta disponible entre ambos servidores.")
        return resultado

    ruta = resultado["ruta"]

    if len(ruta) == 1:
        print("El origen y el destino son el mismo servidor. No se necesitan saltos.")
        print("Latencia total: 0 ms")
        return resultado

    for posicion in range(len(ruta) - 1):
        latencia = resultado["latencias_por_salto"][posicion]
        print(f"Salto {posicion + 1}: {ruta[posicion]} -> {ruta[posicion + 1]} ({latencia} ms)")

    print("Ruta:", " -> ".join(ruta))
    print(f"Latencia total: {resultado['latencia_total']} ms")

    return resultado
    
