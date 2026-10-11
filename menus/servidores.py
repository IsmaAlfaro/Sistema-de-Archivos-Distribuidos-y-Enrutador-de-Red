"""Selección de uno de los servidores compartidos por la aplicación."""
from menus.consola import lin, limpiarConsola, pausarConsola


# Qué hace: muestra los servidores y valida la selección del usuario.
# Recibe: servidores, una lista de objetos Servidor.
# Por teclado: el número del servidor o 0 para volver.
# Devuelve: el objeto Servidor elegido o None si se selecciona 0.
def seleccionarServidor(servidores):
    while True:
        limpiarConsola()
        print(lin)
        print("              SELECCIONAR SERVIDOR")
        print(lin)
        for indice in range(len(servidores)):
            print(f"{indice + 1}. {servidores[indice].nombre}")
        print("0. Volver")
        print(lin)
        opcion = input("Seleccione un servidor: ").strip()
        if opcion == "0":
            return None
        try:
            numero = int(opcion)
        except ValueError:
            print("Ingrese un número válido.")
            pausarConsola()
            continue
        if 1 <= numero <= len(servidores):
            return servidores[numero - 1]
        print("Opción inválida.")
        pausarConsola()
