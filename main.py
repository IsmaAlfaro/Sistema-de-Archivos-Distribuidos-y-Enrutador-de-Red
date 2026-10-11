"""Punto de entrada: construye los componentes y abre el menú principal."""
from estructuras.servidor import Servidor
from estructuras.grafo_red import GrafoRed
from servicios import auditoria
from menus.principal import menuPrincipal


def main():
    # La inicialización no genera eventos de auditoría.
    auditoria.configurar_auditoria(False)
    servidores = [
        Servidor("Servidor 1"),
        Servidor("Servidor 2"),
        Servidor("Servidor 3"),
    ]
    red = GrafoRed()
    for servidor in servidores:
        red.agregar_servidor(servidor)

    # Todos los menús trabajan con los mismos objetos durante la ejecución.
    auditoria.configurar_auditoria(True)
    menuPrincipal(servidores, red)


if __name__ == "__main__":
    main()
