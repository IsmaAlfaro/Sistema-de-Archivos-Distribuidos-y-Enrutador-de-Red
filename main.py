from servidor import Servidor
from grafo import GrafoRed


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


def menu_red(grafo):
    while True:
        print("\n==================================================")
        print("                  RED DE SERVIDORES")
        print("==================================================")
        print("1. Agregar conexión")
        print("2. Eliminar conexión")
        print("3. Mostrar red")
        print("0. Volver")
        print("==================================================")

        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            servidor1 = input("Servidor de origen: ")
            servidor2 = input("Servidor de destino: ")

            try:
                latencia = int(input("Latencia en milisegundos: "))
            except ValueError:
                print("La latencia debe ser un número.")
                continue

            resultado = grafo.agregar_conexion(
                servidor1,
                servidor2,
                latencia
            )

            if resultado:
                print("Conexión agregada correctamente.")
            else:
                print("No se pudo agregar la conexión.")

        elif opcion == "2":
            servidor1 = input("Primer servidor: ")
            servidor2 = input("Segundo servidor: ")

            resultado = grafo.eliminar_conexion(
                servidor1,
                servidor2
            )

            if resultado:
                print("Conexión eliminada correctamente.")
            else:
                print("No se pudo eliminar la conexión.")

        elif opcion == "3":
            print("\nRed actual:")
            grafo.mostrar_red()

        elif opcion == "0":
            break

        else:
            print("Opción inválida.")


def main():
    servidores = [
        Servidor("Servidor 1"),
        Servidor("Servidor 2"),
        Servidor("Servidor 3")
    ]

    grafo = GrafoRed()

    for servidor in servidores:
        grafo.agregar_servidor(servidor)

    while True:
        print("\n==================================================")
        print("                   NETWORK OS")
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
            menu_red(grafo)

        elif opcion == "0":
            print("Saliendo del sistema...")
            break

        else:
            print("Opción inválida.")


if __name__ == "__main__":
    main()