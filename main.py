from servidor import Servidor
from grafo_red import GrafoRed

def menu_archivos(servidor):
    while True:
        print("\n==================================================")
        print("              SISTEMA DE ARCHIVOS")
        print("==================================================")
        print("Servidor:", servidor.nombre)
        print("1. Crear carpeta")
        print("2. Crear archivo")
        print("3. Buscar archivo o carpeta")
        print("4. Mostrar estructura")
        print("5. Eliminar archivo o carpeta")
        print("0. Cerrar sesión")
        print("==================================================")

        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            nombre = input("Nombre de la carpeta: ")
            ruta = input("Ruta donde desea crearla: ")

            resultado = servidor.crear_nodo(nombre, True, ruta)

            if resultado:
                print("Carpeta creada correctamente.")
            else:
                print("No se pudo crear la carpeta.")

        elif opcion == "2":
            nombre = input("Nombre del archivo: ")
            ruta = input("Ruta donde desea crearlo: ")

            resultado = servidor.crear_nodo(nombre, False, ruta)

            if resultado:
                print("Archivo creado correctamente.")
            else:
                print("No se pudo crear el archivo.")

        elif opcion == "3":
            nombre = input("Nombre del archivo o carpeta que desea buscar: ")

            resultado = servidor.buscar_nodo(nombre)

            if resultado is not None:
                print("Archivo o carpeta encontrado:", resultado.nombre)
            else:
                print("Archivo o carpeta no encontrado.")

        elif opcion == "4":
            print("\nEstructura del servidor:")
            servidor.mostrar_estructura()

        elif opcion == "5":
            ruta = input("Ruta del archivo o carpeta que desea eliminar: ")

            resultado = servidor.eliminar_nodo(ruta)

            if resultado:
                print("Archivo o carpeta eliminado correctamente.")
            else:
                print("No se pudo eliminar el archivo o carpeta.")

        elif opcion == "0":
            print("Sesión cerrada.")
            break

        else:
            print("Opción inválida.")


def menu_autenticacion(servidor):
    while True:
        print("\n==================================================")
        print("           NETWORK OS - AUTENTICACIÓN")
        print("==================================================")
        print("Servidor seleccionado:", servidor.nombre)
        print("1. Iniciar Sesión")
        print("2. Registrar Nuevo Usuario")
        print("3. Volver")
        print("==================================================")

        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            usuario = input("Usuario: ")
            contraseña = input("Contraseña: ")

            if servidor.usuarios.autenticar(usuario, contraseña):
                print("Inicio de sesión correcto.")
                menu_archivos(servidor)
            else:
                print("Usuario o contraseña incorrectos.")

        elif opcion == "2":
            usuario = input("Nuevo usuario: ")
            contraseña = input("Contraseña: ")

            resultado = servidor.usuarios.registrar_usuario(
                usuario, contraseña
            )

            if resultado:
                print("Usuario registrado correctamente.")
            else:
                print("El usuario ya existe.")

        elif opcion == "3":
            break

        else:
            print("Opción inválida.")


def seleccionar_servidor(servidores):
    while True:
        print("\n==================================================")
        print("              SELECCIONAR SERVIDOR")
        print("==================================================")

        for i in range(len(servidores)):
            print(f"{i + 1}. {servidores[i].nombre}")

        print("0. Volver")
        print("==================================================")

        opcion = input("Seleccione un servidor: ")

        if opcion == "0":
            return None

        if opcion.isdigit():
            numero = int(opcion)

            if 1 <= numero <= len(servidores):
                return servidores[numero - 1]

        print("Opción inválida.")

def menu_red(red):
    while True:
        print("\n==================================================")
        print("              ADMINISTRACIÓN DE RED")
        print("==================================================")

        print("Servidores disponibles:")
        for servidor in red.servidores:
            print("-", servidor.nombre)

        print("\n1. Agregar conexión")
        print("2. Eliminar conexión")
        print("3. Diagnosticar red")
        print("0. Volver")
        print("==================================================")

        opcion = input("Seleccione una opción: ").strip()

        match opcion:
            case "1":
                origen = input("Nombre del servidor de origen: ").strip()
                destino = input("Nombre del servidor de destino: ").strip()

                try:
                    latencia = float(input("Latencia en milisegundos: "))
                except ValueError:
                    print("La latencia debe ser un número.")
                    continue

                try:
                    mensaje = red.agregar_conexion(
                        origen, destino, latencia
                    )
                    print(mensaje)
                except ValueError as error:
                    print(error)

            case "2":
                origen = input("Nombre del servidor de origen: ").strip()
                destino = input("Nombre del servidor de destino: ").strip()

                try:
                    mensaje = red.eliminar_conexion(origen, destino)
                    print(mensaje)
                except ValueError as error:
                    print(error)

            case "3":
                origen = input(
                    "Nombre del servidor desde donde iniciar: "
                ).strip()

                try:
                    resultado = red.diagnosticar_red(origen)

                    print("\nOrden de visita BFS:")
                    print(" -> ".join(resultado["recorrido"]))

                    if resultado["red_conectada"]:
                        print("Todos los servidores están comunicados.")
                    else:
                        print("La red no está completamente conectada.")

                    print("\nServidores no alcanzables desde el origen:")
                    if resultado["no_alcanzables"]:
                        for nombre in resultado["no_alcanzables"]:
                            print("-", nombre)
                    else:
                        print("Ninguno.")

                    print("\nServidores aislados, sin conexiones:")
                    if resultado["aislados"]:
                        for nombre in resultado["aislados"]:
                            print("-", nombre)
                    else:
                        print("Ninguno.")

                except ValueError as error:
                    print(error)

            case "0":
                print("Volviendo al menú principal...")
                break

            case _:
                print("Opción inválida.")
def main():
    servidores = [
        Servidor("Servidor 1"),
        Servidor("Servidor 2"),
        Servidor("Servidor 3")
    ]

    red = GrafoRed()

    for servidor in servidores:
        red.agregar_servidor(servidor)

    while True:
        print("\n==================================================")
        print("               NETWORK OS")
        print("==================================================")
        print("1. Acceder a un servidor")
        print("2. Administrar red")
        print("0. Salir")
        print("==================================================")

        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            servidor = seleccionar_servidor(servidores)

            if servidor is not None:
                menu_autenticacion(servidor)

        elif opcion == "2":
            menu_red(red)

        elif opcion == "0":
            print("Saliendo del sistema...")
            break

        else:
            print("Opción inválida.")


if __name__ == "__main__":
    main()