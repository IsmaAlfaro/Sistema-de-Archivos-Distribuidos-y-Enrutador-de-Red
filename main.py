import os
from datetime import datetime as fechaHora

from servidor import Servidor
from grafo_red import GrafoRed
from enrutamiento import simular_envio_paquete as simularEnvioPaquete
import auditoria as moduloAuditoria


lin = "------------------------------------------"


def limpiarConsola():
    os.system("cls")


def pausarConsola():
    input("\nPresione Enter para continuar...")


def ingresarFecha():
    while True:
        fecha = input("Ingrese la fecha (dd:mm:aaaa): ").strip()

        try:
            fechaTemp = fechaHora.strptime(fecha, "%d:%m:%Y")

            if fechaTemp.strftime("%d:%m:%Y") == fecha:
                return fecha
        except ValueError:
            pass

        print("Fecha inválida. Use el formato dd:mm:aaaa.")


def menuArchivos(servidor):
    while True:
        limpiarConsola()
        print(lin)
        print("              SISTEMA DE ARCHIVOS")
        print(lin)
        print("Servidor:", servidor.nombre)
        print("1. Crear carpeta")
        print("2. Crear archivo")
        print("3. Buscar archivo o carpeta")
        print("4. Mostrar estructura")
        print("5. Eliminar archivo o carpeta")
        print("0. Cerrar sesión")
        print(lin)

        opcion = input("Seleccione una opción: ").strip()

        if opcion == "1":
            nombre = input("Nombre de la carpeta: ")
            ruta = input("Ruta donde desea crearla: ")

            resultado = servidor.crear_nodo(nombre, True, ruta)

            if resultado:
                print("Carpeta creada correctamente.")
            else:
                print("No se pudo crear la carpeta.")

            pausarConsola()

        elif opcion == "2":
            nombre = input("Nombre del archivo: ")
            ruta = input("Ruta donde desea crearlo: ")

            resultado = servidor.crear_nodo(nombre, False, ruta)

            if resultado:
                print("Archivo creado correctamente.")
            else:
                print("No se pudo crear el archivo.")

            pausarConsola()

        elif opcion == "3":
            nombre = input(
                "Nombre del archivo o carpeta que desea buscar: "
            )

            resultado = servidor.buscar_nodo(nombre)

            if resultado is not None:
                print("Archivo o carpeta encontrado:", resultado.nombre)
            else:
                print("Archivo o carpeta no encontrado.")

            pausarConsola()

        elif opcion == "4":
            print("\nEstructura del servidor:")
            servidor.mostrar_estructura()
            pausarConsola()

        elif opcion == "5":
            ruta = input("Ruta del archivo o carpeta que desea eliminar: ")

            resultado = servidor.eliminar_nodo(ruta)

            if resultado:
                print("Archivo o carpeta eliminado correctamente.")
            else:
                print("No se pudo eliminar el archivo o carpeta.")

            pausarConsola()

        elif opcion == "0":
            print("Sesión cerrada.")
            break

        else:
            print("Opción inválida.")
            pausarConsola()


def menuAutenticacion(servidor):
    while True:
        limpiarConsola()
        print(lin)
        print("           NETWORK OS - AUTENTICACIÓN")
        print(lin)
        print("Servidor seleccionado:", servidor.nombre)
        print("1. Iniciar Sesión")
        print("2. Registrar Nuevo Usuario")
        print("3. Volver")
        print(lin)

        opcion = input("Seleccione una opción: ").strip()

        if opcion == "1":
            usuario = input("Usuario: ")
            contraseña = input("Contraseña: ")

            if servidor.usuarios.autenticar(usuario, contraseña):
                print("Inicio de sesión correcto.")
                pausarConsola()
                menuArchivos(servidor)
            else:
                print("Usuario o contraseña incorrectos.")
                pausarConsola()

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

            pausarConsola()

        elif opcion == "3":
            break

        else:
            print("Opción inválida.")
            pausarConsola()


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

        if opcion.isdigit():
            numero = int(opcion)

            if 1 <= numero <= len(servidores):
                return servidores[numero - 1]

        print("Opción inválida.")
        pausarConsola()


def menuRed(red):
    while True:
        limpiarConsola()
        print(lin)
        print("              ADMINISTRACIÓN DE RED")
        print(lin)

        print("Servidores disponibles:")
        for servidor in red.servidores:
            print("-", servidor.nombre)

        print("\n1. Agregar conexión")
        print("2. Eliminar conexión")
        print("3. Diagnosticar red")
        print("4. Simular envío de paquete")
        print("0. Volver")
        print(lin)

        opcion = input("Seleccione una opción: ").strip()

        match opcion:
            case "1":
                origen = input(
                    "Nombre del servidor de origen: "
                ).strip()
                destino = input(
                    "Nombre del servidor de destino: "
                ).strip()

                try:
                    latencia = float(
                        input("Latencia en milisegundos: ")
                    )
                except ValueError:
                    print("La latencia debe ser un número.")
                    pausarConsola()
                    continue

                try:
                    mensaje = red.agregar_conexion(
                        origen, destino, latencia
                    )
                    print(mensaje)
                except ValueError as error:
                    print(error)

                pausarConsola()

            case "2":
                origen = input(
                    "Nombre del servidor de origen: "
                ).strip()
                destino = input(
                    "Nombre del servidor de destino: "
                ).strip()

                try:
                    mensaje = red.eliminar_conexion(origen, destino)
                    print(mensaje)
                except ValueError as error:
                    print(error)

                pausarConsola()

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

                pausarConsola()

            case "4":
                origen = input(
                    "Nombre del servidor de origen: "
                ).strip()
                destino = input(
                    "Nombre del servidor de destino: "
                ).strip()

                try:
                    simularEnvioPaquete(red, origen, destino)
                except ValueError as error:
                    print(error)

                pausarConsola()

            case "0":
                print("Volviendo al menú principal...")
                break

            case _:
                print("Opción inválida.")
                pausarConsola()


def menuAuditoria():
    while True:
        limpiarConsola()
        print(lin)
        print("              SISTEMA DE AUDITORÍA")
        print(lin)
        print("1. Leer todo el registro")
        print("2. Leer desde una fecha en adelante")
        print("3. Leer los registros de una fecha")
        print("0. Volver")
        print(lin)

        opcion = input("Seleccione una opción: ").strip()

        try:
            if opcion == "1":
                moduloAuditoria.leerRegistro()
                pausarConsola()

            elif opcion == "2":
                metodoLectura = getattr(
                    moduloAuditoria, "leerRegistroDesde", None
                )

                if metodoLectura is None:
                    print("La lectura del registro por fecha aún no está disponible.")
                else:
                    fecha = ingresarFecha()
                    metodoLectura(fecha)

                pausarConsola()

            elif opcion == "3":
                metodoLectura = getattr(
                    moduloAuditoria, "leerRegistroFecha", None
                )

                if metodoLectura is None:
                    print("La lectura del registro por fecha aún no está disponible.")
                else:
                    fecha = ingresarFecha()
                    metodoLectura(fecha)

                pausarConsola()

            elif opcion == "0":
                break

            else:
                print("Opción inválida.")
                pausarConsola()

        except OSError as error:
            print(error)
            pausarConsola()


def main():
    moduloAuditoria.configurar_auditoria(False)

    servidores = [
        Servidor("Servidor 1"),
        Servidor("Servidor 2"),
        Servidor("Servidor 3")
    ]

    red = GrafoRed()

    for servidor in servidores:
        red.agregar_servidor(servidor)

    moduloAuditoria.configurar_auditoria(True)

    while True:
        limpiarConsola()
        print(lin)
        print("               NETWORK OS")
        print(lin)
        print("1. Acceder a un servidor")
        print("2. Administrar red")
        print("3. Consultar auditoría")
        print("0. Salir")
        print(lin)

        opcion = input("Seleccione una opción: ").strip()

        if opcion == "1":
            servidor = seleccionarServidor(servidores)

            if servidor is not None:
                menuAutenticacion(servidor)

        elif opcion == "2":
            menuRed(red)

        elif opcion == "3":
            menuAuditoria()

        elif opcion == "0":
            print("Saliendo del sistema...")
            break

        else:
            print("Opción inválida.")
            pausarConsola()


if __name__ == "__main__":
    main()
    
