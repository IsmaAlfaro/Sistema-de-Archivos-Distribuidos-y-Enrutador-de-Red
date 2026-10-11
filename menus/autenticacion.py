"""Registro e inicio de sesión de los usuarios de un servidor."""
from menus.archivos import menuArchivos
from menus.consola import lin, limpiarConsola, pausarConsola, leerContrasena


# Abre archivos solo si la autenticación se completa; 3 vuelve al principal.
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
                    autenticado = servidor.usuarios.autenticar(usuario, contraseña)
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
                    resultado = servidor.usuarios.registrar_usuario(usuario, contraseña)
                except ValueError as error:
                    print(error)
                    pausarConsola()
                    continue
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
