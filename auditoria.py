from datetime import datetime
from pathlib import Path


def registrar_evento(origen, accion):
    ruta_archivo = Path(__file__).resolve().with_name( #se asiga la ruta y nombre del archivo
        "network_audit_log.txt"
    )

    try:                                            #se revisa si existe el archivo, de lo contrario se crea.
        if not ruta_archivo.exists():
            ruta_archivo.touch()
    except OSError as error:
        raise OSError(
            "Error! El archivo no se pudo abrir con exito."
        ) from error

    try:                                            #se intenta abrir el archivo y en caso de que falle, se tira un error.
        archivo = ruta_archivo.open("a+", encoding="utf-8")
    except OSError as error:
        raise OSError(
            "Error! El archivo no se pudo abrir con exito."
        ) from error

    fecha_hora = datetime.now().strftime("%d:%m:%Y %H:%M:%S")      #Se obtiene la fecha y hora de la accion
    registro = f"{origen}~{accion}~{fecha_hora}~\n"                #Se formatea el registro de la accion hecha usando '~' como separador

    with archivo:                  #Se busca la linea vacia mas cercana disponible
        archivo.seek(0)
        contenido = archivo.read()

        if contenido and not contenido.endswith("\n"):
            archivo.write("\n")

        archivo.write(registro)          #Se escribe en el archivo el registro.

    return True
    
def leer_registro():
  ...
    
