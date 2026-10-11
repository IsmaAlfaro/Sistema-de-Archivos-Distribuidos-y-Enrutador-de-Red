"""Selección de uno de los servidores compartidos por la aplicación."""
from menus.consola import lin, limpiarConsola, pausarConsola


# Devuelve el servidor elegido o None al seleccionar 0.
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
