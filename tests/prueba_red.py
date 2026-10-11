# Pruebas secuenciales de conexiones y BFS: ejecutar python -m tests.prueba_red.
# Los bloques comparten la misma red; cada escenario parte del estado del anterior.
# assert verifica resultados y try/except comprueba los ValueError esperados.
# La auditoría permanece desactivada por defecto al iniciar este proceso.
from estructuras.servidor import Servidor
from estructuras.grafo_red import GrafoRed


red = GrafoRed()

servidor1 = Servidor("Servidor 1")
servidor2 = Servidor("Servidor 2")
servidor3 = Servidor("Servidor 3")

# Registrar los servidores.
print(red.agregar_servidor(servidor1))
print(red.agregar_servidor(servidor2))
print(red.agregar_servidor(servidor3))

# Crear conexiones.
print(red.agregar_conexion("Servidor 1", "Servidor 2", 10))
print(red.agregar_conexion("Servidor 1", "Servidor 3", 20))

# Verificar que las conexiones estén en ambas direcciones.
print("Adyacencias:", red.adyacencias)

assert red.adyacencias == [
    [(1, 10), (2, 20)],
    [(0, 10)],
    [(0, 20)]
]

print("Conexiones guardadas correctamente.")

# Probar validaciones.
casos_invalidos = [
    ("Servidor 1", "Servidor 2", 10),  # Conexión duplicada.
    ("Servidor 2", "Servidor 1", 10),  # Duplicada en sentido inverso.
    ("Servidor 1", "Servidor 4", 10),  # Servidor inexistente.
    ("Servidor 1", "Servidor 1", 10),  # Conexión consigo mismo.
    ("Servidor 2", "Servidor 3", -5),  # Latencia negativa.
    ("Servidor 2", "Servidor 3", 0),   # Cero: tu validación lo rechaza.
]

for origen, destino, latencia in casos_invalidos:
    try:
        red.agregar_conexion(origen, destino, latencia)
    except ValueError as error:
        print("Error esperado:", error)
    else:
        raise AssertionError(
            f"Se aceptó una conexión inválida: {origen}, {destino}, {latencia}"
        )

# Los intentos inválidos no deben modificar la red.
assert red.adyacencias == [
    [(1, 10), (2, 20)],
    [(0, 10)],
    [(0, 20)]
]

print("Todas las pruebas pasaron.")

# Eliminar una conexión existente.
print(red.eliminar_conexion("Servidor 1", "Servidor 2"))

# Debe desaparecer en ambos sentidos y conservarse la otra conexión.
assert red.adyacencias == [
    [(2, 20)],  # Servidor 1 conserva su conexión con Servidor 3.
    [],         # Servidor 2 queda sin conexiones.
    [(0, 20)]   # Servidor 3 conserva su conexión con Servidor 1.
]

# Eliminar un enlace no debe eliminar los servidores.
assert len(red.servidores) == 3

# Comprobar los casos inválidos.
casos_eliminacion_invalidos = [
    ("Servidor 1", "Servidor 2"),  # Ya se eliminó.
    ("Servidor 2", "Servidor 1"),  # Tampoco existe en sentido inverso.
    ("Servidor 1", "Servidor 4"),  # El servidor no existe.
]

for origen, destino in casos_eliminacion_invalidos:
    try:
        red.eliminar_conexion(origen, destino)
    except ValueError as error:
        print("Error esperado:", error)
    else:
        raise AssertionError(
            f"Se aceptó una eliminación inválida: {origen}, {destino}"
        )

# Los intentos inválidos no deben modificar la red.
assert red.adyacencias == [
    [(2, 20)],
    [],
    [(0, 20)]
]

print("Pruebas de eliminación completadas correctamente.")

# 1. Red desconectada: Servidor 2 está aislado.
resultado = red.diagnosticar_red("Servidor 1")
print("Diagnóstico inicial:", resultado)

assert resultado["recorrido"] == ["Servidor 1", "Servidor 3"]
assert resultado["no_alcanzables"] == ["Servidor 2"]
assert resultado["aislados"] == ["Servidor 2"]
assert resultado["red_conectada"] is False

# 2. Reconectar la red.
red.agregar_conexion("Servidor 2", "Servidor 3", 15)

resultado = red.diagnosticar_red("Servidor 1")

assert resultado["recorrido"] == [
    "Servidor 1", "Servidor 3", "Servidor 2"
]
assert resultado["no_alcanzables"] == []
assert resultado["aislados"] == []
assert resultado["red_conectada"] is True

# 3. Crear un grupo separado, cuyos servidores no estén aislados.
red.agregar_servidor(Servidor("Servidor 4"))
red.agregar_servidor(Servidor("Servidor 5"))
red.agregar_conexion("Servidor 4", "Servidor 5", 8)

resultado = red.diagnosticar_red("Servidor 1")

assert resultado["no_alcanzables"] == ["Servidor 4", "Servidor 5"]
assert resultado["aislados"] == []
assert resultado["red_conectada"] is False

# 4. Un ciclo no debe provocar visitas repetidas.
red.agregar_conexion("Servidor 1", "Servidor 2", 10)

resultado = red.diagnosticar_red("Servidor 1")

assert len(resultado["recorrido"]) == 3
assert set(resultado["recorrido"]) == {
    "Servidor 1", "Servidor 2", "Servidor 3"
}

# 5. Rechazar un origen inexistente.
try:
    red.diagnosticar_red("Servidor inexistente")
except ValueError as error:
    print("Error esperado:", error)
else:
    raise AssertionError("Se aceptó un servidor de origen inexistente.")

print("Pruebas de diagnóstico completadas correctamente.")
