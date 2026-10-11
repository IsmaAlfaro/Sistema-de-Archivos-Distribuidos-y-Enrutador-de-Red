"""Administración de conexiones, diagnóstico y simulación de envío."""
from servicios.enrutamiento import simular_envio_paquete as simularEnvioPaquete
from menus.consola import lin, limpiarConsola, pausarConsola


# Recibe la red compartida y conserva su estado al entrar o salir del menú.
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
                origen = input("Nombre del servidor de origen: ").strip()
                destino = input("Nombre del servidor de destino: ").strip()
                try:
                    latencia = float(input("Latencia en milisegundos: "))
                except ValueError:
                    print("La latencia debe ser un número.")
                    pausarConsola()
                    continue
                try:
                    mensaje = red.agregar_conexion(origen, destino, latencia)
                    print(mensaje)
                except ValueError as error:
                    print(error)
                except OSError as error:
                    print("Error de auditoría:", error)
                pausarConsola()

            case "2":
                origen = input("Nombre del servidor de origen: ").strip()
                destino = input("Nombre del servidor de destino: ").strip()
                try:
                    mensaje = red.eliminar_conexion(origen, destino)
                    print(mensaje)
                except ValueError as error:
                    print(error)
                except OSError as error:
                    print("Error de auditoría:", error)
                pausarConsola()

            case "3":
                origen = input("Nombre del servidor desde donde iniciar: ").strip()
                try:
                    resultado = red.diagnosticar_red(origen)
                    print("\nOrden de visita BFS:")
                    # Es un orden de exploración, no una ruta entre saltos.
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
                origen = input("Nombre del servidor de origen: ").strip()
                destino = input("Nombre del servidor de destino: ").strip()
                try:
                    simularEnvioPaquete(red, origen, destino)
                except ValueError as error:
                    print(error)
                except OSError as error:
                    print("Error de auditoría:", error)
                pausarConsola()

            case "0":
                print("Volviendo al menú principal...")
                break

            case _:
                print("Opción inválida.")
                pausarConsola()
