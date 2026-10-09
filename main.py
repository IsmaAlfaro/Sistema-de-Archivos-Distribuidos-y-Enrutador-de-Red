# Interfaz de consola: solicita datos y delega las operaciones en los módulos.
# Requiere Python 3.10 o superior por la selección con match/case del menú de red.
import os
from datetime import datetime as fechaHora

from servidor import Servidor
from grafo_red import GrafoRed
from enrutamiento import simular_envio_paquete as simularEnvioPaquete
from msvcrt import getwch
import auditoria as moduloAuditoria


lin = "------------------------------------------"


# Limpia la pantalla mediante el comando de Windows cls. No devuelve un valor.
def limpiarConsola():
    os.system("cls")


# Espera Enter para que el usuario pueda leer el resultado antes de limpiar la pantalla.
def pausarConsola():
    input("\nPresione Enter para continuar...")


# Solicita una fecha hasta que sea válida y devuelve su texto en formato dd:mm:aaaa.
# La comparación con strftime exige el formato completo, incluidos los ceros iniciales.
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


# Administra los archivos y carpetas del servidor recibido.
# Selecciona operaciones con match/case y maneja errores de auditoría.
# La opción 0 cierra la sesión y retorna al menú de autenticación.
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

        match opcion:
            case "1":
                nombre = input("Nombre de la carpeta: ")
                ruta = input("Ruta donde desea crearla: ")

                try:
                    resultado = servidor.crear_nodo(nombre, True, ruta)
                except OSError as error:
                    print("No se pudo completar la creación de la carpeta.")
                    print("Error de auditoría:", error)
                    pausarConsola()
                    continue

                if resultado:
                    print("Carpeta creada correctamente.")
                else:
                    print("No se pudo crear la carpeta.")

                pausarConsola()

            case "2":
                nombre = input("Nombre del archivo: ")
                ruta = input("Ruta donde desea crearlo: ")

                try:
                    resultado = servidor.crear_nodo(nombre, False, ruta)
                except OSError as error:
                    print("No se pudo completar la creación del archivo.")
                    print("Error de auditoría:", error)
                    pausarConsola()
                    continue

                if resultado:
                    print("Archivo creado correctamente.")
                else:
                    print("No se pudo crear el archivo.")

                pausarConsola()

            case "3":
                nombre = input(
                    "Nombre del archivo o carpeta que desea buscar: "
                )

                resultado = servidor.buscar_nodo(nombre)

                if resultado is not None:
                    print("Archivo o carpeta encontrado:", resultado.nombre)
                else:
                    print("Archivo o carpeta no encontrado.")

                pausarConsola()

            case "4":
                print("\nEstructura del servidor:")
                servidor.mostrar_estructura()
                pausarConsola()

            case "5":
                ruta = input(
                    "Ruta del archivo o carpeta que desea eliminar: "
                )

                try:
                    resultado = servidor.eliminar_nodo(ruta)
                except OSError as error:
                    print("No se pudo completar la eliminación.")
                    print("Error de auditoría:", error)
                    pausarConsola()
                    continue

                if resultado:
                    print("Archivo o carpeta eliminado correctamente.")
                else:
                    print("No se pudo eliminar el archivo o carpeta.")

                pausarConsola()

            case "0":
                print("Sesión cerrada.")
                break

            case _:
                print("Opción inválida.")
                pausarConsola()


# Solicita una contraseña mostrando un asterisco por cada carácter.
# Permite borrar con Retroceso y devuelve el texto original al pulsar Enter.
# Utiliza la consola de Windows; Ctrl+C interrumpe la captura.
def leerContrasena(mensaje="Contraseña: "):
    print(mensaje, end="", flush=True)
    caracteres = []

    while True:
        caracter = getwch()

        # Enter termina la captura.
        if caracter in ("\r", "\n"):
            print()
            return "".join(caracteres)

        # Ctrl+C permite interrumpir la operación.
        if caracter == "\x03":
            print()
            raise KeyboardInterrupt

        # Flechas y otras teclas especiales generan una secuencia de dos códigos.
        if caracter in ("\x00", "\xe0"):
            getwch()
            continue

        # Retroceso elimina el último carácter y su asterisco.
        if caracter == "\b":
            if caracteres:
                caracteres.pop()
                print("\b \b", end="", flush=True)
            continue

        # Guarda caracteres imprimibles, incluidos espacios.
        if caracter.isprintable():
            caracteres.append(caracter)
            print("*", end="", flush=True)

# Registra o autentica usuarios en la tabla hash del servidor recibido.
# Maneja fallos de auditoría y abre archivos solo si la autenticación se completa.
# La opción 3 retorna al menú principal.
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

        match opcion:
            case "1":
                usuario = input("Usuario: ")
                contraseña = leerContrasena("Contraseña: ")

                try:
                    autenticado = servidor.usuarios.autenticar(
                        usuario, contraseña
                    )
                except OSError as error:
                    print("No se pudo completar el inicio de sesión.")
                    print("Error de auditoría:", error)
                    pausarConsola()
                    continue

                if autenticado:
                    print("Inicio de sesión correcto.")
                    pausarConsola()
                    menuArchivos(servidor)
                else:
                    print("Usuario o contraseña incorrectos.")
                    pausarConsola()

            case "2":
                usuario = input("Nuevo usuario: ")
                contraseña = leerContrasena("Contraseña: ")

                try:
                    resultado = servidor.usuarios.registrar_usuario(
                        usuario, contraseña
                    )
                except OSError as error:
                    print("No se pudo completar el registro del usuario.")
                    print("Error de auditoría:", error)
                    pausarConsola()
                    continue

                if resultado:
                    print("Usuario registrado correctamente.")
                else:
                    print("El usuario ya existe.")

                pausarConsola()

            case "3":
                break

            case _:
                print("Opción inválida.")
                pausarConsola()


# Muestra la lista recibida y devuelve el objeto Servidor elegido por su número.
# Devuelve None al seleccionar 0; las opciones fuera de rango vuelven a solicitarse.
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


# Recibe la red compartida y permite conectar, desconectar, diagnosticar y enviar.
# Convierte la latencia a float y maneja ValueError y fallos de auditoría OSError.
# Al volver, conserva la instancia recibida y sus conexiones; no devuelve datos.
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
            # Cada case termina por sí mismo; no requiere break como un switch de C.
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

                except OSError as error:
                    print("Error de auditoría:", error)

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

                except OSError as error:
                    print("Error de auditoría:", error)

                pausarConsola()

            case "3":
                origen = input(
                    "Nombre del servidor desde donde iniciar: "
                ).strip()

                try:
                    resultado = red.diagnosticar_red(origen)

                    print("\nOrden de visita BFS:")
                    # Es un orden de exploración, no necesariamente una ruta entre saltos.
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

                except OSError as error:
                    print("Error de auditoría:", error)

                pausarConsola()

            case "0":
                # Este break termina el while del menú, no solamente el match.
                print("Volviendo al menú principal...")
                break

            case _:
                print("Opción inválida.")
                pausarConsola()


# Consulta el historial completo o filtrado por fecha, sin modificar sus registros.
# Comprueba si existen los métodos de filtrado y captura errores de acceso al archivo.
# La opción 0 retorna al menú principal sin devolver datos.
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




# Crea los servidores y la red compartida antes de abrir el menú principal.
# Activa la auditoría después de la inicialización.
# Selecciona con match/case el área del sistema que desea utilizar el usuario.
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

        match opcion:
            case "1":
                servidor = seleccionarServidor(servidores)

                if servidor is not None:
                    menuAutenticacion(servidor)

            case "2":
                menuRed(red)

            case "3":
                menuAuditoria()

            case "0":
                print("Saliendo del sistema...")
                break

            case _:
                print("Opción inválida.")
                pausarConsola()


# Inicia la interfaz solo al ejecutar este archivo, no al importarlo desde pruebas.
if __name__ == "__main__":
    main()
    
