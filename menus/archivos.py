"""Menú de archivos y carpetas del servidor autenticado."""
from menus.consola import lin, limpiarConsola, pausarConsola


# Qué hace: permite crear, buscar, mostrar y eliminar archivos o carpetas.
# Recibe: servidor, el objeto Servidor sobre cuyo árbol se realizan las operaciones.
# Por teclado: la opción del menú y los nombres o rutas necesarios para cada operación.
# Devuelve: nada; la opción 0 cierra la sesión y vuelve al menú de autenticación.
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
                nombre = input("Nombre del archivo o carpeta que desea buscar: ")
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
                ruta = input("Ruta del archivo o carpeta que desea eliminar: ")
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
