# Pruebas de enrutamiento: ejecutar python -m tests.practica_enrutamiento desde la raíz.
# Cada assert comprueba un resultado y detiene el script si no coincide.
# La auditoría permanece desactivada por defecto al iniciar este proceso.
from estructuras.servidor import Servidor
from estructuras.grafo_red import GrafoRed
from servicios.enrutamiento import (
    dijkstra, reconstruir_ruta, calcular_ruta, simular_envio_paquete, INFINITO
)


# Recibe la cantidad de servidores y tuplas (numero_origen, numero_destino, latencia).
# Los números empiezan en 1; devuelve un GrafoRed nuevo para aislar cada escenario.
# Los nombres usados aquí son distintos de los índices internos, que empiezan en 0.
def construir_red(cantidad, conexiones):
    """Crea una red con 'Servidor 1'...'Servidor N' y las conexiones indicadas."""
    red = GrafoRed()
    for numero in range(1, cantidad + 1):
        red.agregar_servidor(Servidor(f"Servidor {numero}"))
    for origen, destino, latencia in conexiones:
        red.agregar_conexion(f"Servidor {origen}", f"Servidor {destino}", latencia)
    return red


# Caso 1: ruta directa.
red = construir_red(2, [(1, 2, 10)])
resultado = calcular_ruta(red, "Servidor 1", "Servidor 2")
assert resultado["hay_ruta"] is True
assert resultado["ruta"] == ["Servidor 1", "Servidor 2"]
assert resultado["latencia_total"] == 10
assert resultado["latencias_por_salto"] == [10]
print("Caso 1 (ruta directa) correcto.")

# Caso 2: ruta con varios saltos (1 -> 2 -> 4 -> 5).
red = construir_red(5, [(1, 2, 5), (2, 4, 7), (4, 5, 3), (1, 3, 50), (3, 5, 50)])
resultado = calcular_ruta(red, "Servidor 1", "Servidor 5")
assert resultado["ruta"] == ["Servidor 1", "Servidor 2", "Servidor 4", "Servidor 5"]
assert resultado["latencia_total"] == 15
assert resultado["latencias_por_salto"] == [5, 7, 3]
print("Caso 2 (varios saltos) correcto.")

# Caso 3: varias rutas, debe escogerse la de menor latencia (20 ms y no 30 ms).
red = construir_red(3, [(1, 2, 10), (2, 3, 10), (1, 3, 30)])
resultado = calcular_ruta(red, "Servidor 1", "Servidor 3")
assert resultado["ruta"] == ["Servidor 1", "Servidor 2", "Servidor 3"]
assert resultado["latencia_total"] == 20

# Caso 3b: la ruta directa es la mejor cuando es más barata que el desvío.
red = construir_red(3, [(1, 2, 10), (2, 3, 10), (1, 3, 15)])
resultado = calcular_ruta(red, "Servidor 1", "Servidor 3")
assert resultado["ruta"] == ["Servidor 1", "Servidor 3"]
assert resultado["latencia_total"] == 15
print("Caso 3 (elige la menor latencia) correcto.")

# La ruta inversa cuesta lo mismo (grafo no dirigido).
red = construir_red(3, [(1, 2, 10), (2, 3, 10), (1, 3, 30)])
inversa = calcular_ruta(red, "Servidor 3", "Servidor 1")
assert inversa["ruta"] == ["Servidor 3", "Servidor 2", "Servidor 1"]
assert inversa["latencia_total"] == 20

# Caso 4: no existe ruta (Servidor 3 está aislado, y Servidor 4-5 forman otro grupo).
red = construir_red(5, [(1, 2, 10), (4, 5, 8)])
resultado = calcular_ruta(red, "Servidor 1", "Servidor 3")
assert resultado["hay_ruta"] is False
assert resultado["ruta"] == []
assert resultado["latencia_total"] is None
resultado = calcular_ruta(red, "Servidor 1", "Servidor 5")
assert resultado["hay_ruta"] is False
print("Caso 4 (sin ruta) correcto.")

# Caso 5: origen y destino iguales.
resultado = calcular_ruta(red, "Servidor 1", "Servidor 1")
assert resultado["hay_ruta"] is True
assert resultado["ruta"] == ["Servidor 1"]
assert resultado["latencia_total"] == 0
print("Caso 5 (origen = destino) correcto.")

# Caso 6: servidores inexistentes.
for origen, destino in [("Servidor 9", "Servidor 1"), ("Servidor 1", "Servidor 9"),
                        ("Servidor 8", "Servidor 9")]:
    try:
        calcular_ruta(red, origen, destino)
    except ValueError as error:
        print("Error esperado:", error)
    else:
        raise AssertionError(f"Se aceptó un servidor inexistente: {origen}, {destino}")

# Red vacía: cualquier servidor es inexistente.
try:
    calcular_ruta(GrafoRed(), "Servidor 1", "Servidor 2")
except ValueError as error:
    print("Error esperado (red vacía):", error)
else:
    raise AssertionError("Se aceptó una consulta sobre una red vacía.")
print("Caso 6 (servidor inexistente) correcto.")

# Pruebas directas de dijkstra: distancias y predecesores.
red = construir_red(4, [(1, 2, 10), (2, 3, 10), (1, 3, 30)])
distancias, predecesores = dijkstra(red, 0)
assert distancias == [0, 10, 20, INFINITO]
assert predecesores == [None, 0, 1, None]
assert reconstruir_ruta(predecesores, 2) == [0, 1, 2]

# Latencias decimales (el menú las convierte con float()).
red = construir_red(3, [(1, 2, 10.5), (2, 3, 4.5)])
resultado = calcular_ruta(red, "Servidor 1", "Servidor 3")
assert resultado["latencia_total"] == 15.0

# El cálculo no debe modificar la red.
red = construir_red(3, [(1, 2, 10), (2, 3, 10), (1, 3, 30)])
antes = [lista[:] for lista in red.adyacencias]
calcular_ruta(red, "Servidor 1", "Servidor 3")
assert red.adyacencias == antes

# Mostrar la simulación completa (revisar la salida a ojo).
simular_envio_paquete(red, "Servidor 1", "Servidor 3")
simular_envio_paquete(red, "Servidor 1", "Servidor 1")
red.agregar_servidor(Servidor("Servidor 4"))
simular_envio_paquete(red, "Servidor 1", "Servidor 4")

print("\nPruebas de enrutamiento completadas correctamente.")
