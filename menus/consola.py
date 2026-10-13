"""Utilidades compartidas de presentación y entrada por consola."""
import os
from datetime import datetime as fechaHora
try:
    from msvcrt import getwch   # Windows: lee tecla por tecla
except ImportError:
    getwch = None               # Linux/macOS: se usa getpass


lin = "------------------------------------------"


# Qué hace: limpia la pantalla de la terminal ejecutando cls en Windows.
# Recibe: ningún parámetro.
# Devuelve: nada.
def limpiarConsola():
    os.system("cls" if os.name == "nt" else "clear")


# Qué hace: pausa el programa para permitir que el usuario lea el resultado.
# Recibe: ningún parámetro; espera que el usuario presione Enter por teclado.
# Devuelve: nada; continúa después de recibir la entrada.
def pausarConsola():
    input("\nPresione Enter para continuar...")


# Qué hace: pide una fecha y repite la solicitud hasta que el formato y el día sean válidos.
# Recibe: ningún parámetro; lee por teclado una fecha con formato dd:mm:aaaa.
# Devuelve: la fecha validada como texto, con los ceros iniciales y sin espacios exteriores.
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


# Qué hace: captura una contraseña mostrando asteriscos y permite borrar con Retroceso.
# Recibe: mensaje (texto del aviso, "Contraseña: " por defecto) y caracteres por teclado.
# Devuelve: la contraseña como texto al pulsar Enter, conservando sus espacios.
# Ctrl+C lanza KeyboardInterrupt; las teclas especiales se ignoran.
def leerContrasena(mensaje="Contraseña: "):
    if getwch is None:
        from getpass import getpass
        return getpass(mensaje)
    print(mensaje, end="", flush=True)
    caracteres = []
    while True:
        caracter = getwch()
        if caracter in ("\r", "\n"):
            print()
            return "".join(caracteres)
        if caracter == "\x03":
            print()
            raise KeyboardInterrupt
        # Flechas y otras teclas especiales generan dos códigos.
        if caracter in ("\x00", "\xe0"):
            getwch()
            continue
        if caracter == "\b":
            if caracteres:
                caracteres.pop()
                print("\b \b", end="", flush=True)
            continue
        if caracter.isprintable():
            caracteres.append(caracter)
            print("*", end="", flush=True)
