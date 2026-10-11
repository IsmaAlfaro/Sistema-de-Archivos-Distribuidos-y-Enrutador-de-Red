"""Menú principal y navegación entre las áreas del sistema."""
from menus.autenticacion import menuAutenticacion
from menus.auditoria import menuAuditoria
from menus.red import menuRed
from menus.servidores import seleccionarServidor
from menus.consola import lin, limpiarConsola, pausarConsola


# Qué hace: muestra el menú principal y abre el área seleccionada por el usuario.
# Recibe: servidores (lista de objetos Servidor) y red (GrafoRed compartido).
# Por teclado: la opción del menú; delega las demás entradas a cada submenú.
# Devuelve: nada; termina al elegir 0 y conserva los objetos recibidos.
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
