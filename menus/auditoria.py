"""Consulta del historial completo o filtrado por fecha."""
from servicios import auditoria as moduloAuditoria
from menus.consola import lin, limpiarConsola, pausarConsola, ingresarFecha


# Consulta el registro y captura errores de acceso al archivo.
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
                metodoLectura = getattr(moduloAuditoria, "leerRegistroDesde", None)
                if metodoLectura is None:
                    print("La lectura del registro por fecha aún no está disponible.")
                else:
                    fecha = ingresarFecha()
                    metodoLectura(fecha)
                pausarConsola()
            elif opcion == "3":
                metodoLectura = getattr(moduloAuditoria, "leerRegistroFecha", None)
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
