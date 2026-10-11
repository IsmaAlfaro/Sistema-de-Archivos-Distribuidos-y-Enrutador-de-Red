"""Utilidades compartidas de presentación y entrada por consola."""
import os
from datetime import datetime as fechaHora
from msvcrt import getwch


lin = "------------------------------------------"


# Limpia la pantalla mediante el comando de Windows cls.
def limpiarConsola():
    os.system("cls")


# Espera Enter para que el usuario pueda leer el resultado.
def pausarConsola():
    input("\nPresione Enter para continuar...")


# Solicita una fecha hasta que sea válida, incluidos los ceros iniciales.
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


# Captura la contraseña con asteriscos, Retroceso y Enter en Windows.
def leerContrasena(mensaje="Contraseña: "):
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
