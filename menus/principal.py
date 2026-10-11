"""Menú principal y navegación entre las áreas del sistema."""
from menus.autenticacion import menuAutenticacion
from menus.auditoria import menuAuditoria
from menus.red import menuRed
from menus.servidores import seleccionarServidor
from menus.consola import lin, limpiarConsola, pausarConsola


# Recibe los objetos inicializados por main; no reconstruye la red ni los usuarios.
def menuPrincipal(servidores, red):
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
