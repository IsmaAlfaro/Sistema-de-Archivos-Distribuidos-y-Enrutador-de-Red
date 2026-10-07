from datetime import datetime
from pathlib import Path


_RUTA_ARCHIVO_PREDETERMINADA = Path(__file__).resolve().with_name(
    "network_audit_log.txt"
)
_ruta_archivo = _RUTA_ARCHIVO_PREDETERMINADA
_auditoria_activa = False                        #False == auditoria desactivada para pruevas unitarias. True == auditoria activada para uso regular del sistema.


def configurar_auditoria(activa, ruta_archivo=None):        #Configuracion de la auditoria para ambiente de pruevas
    global _auditoria_activa, _ruta_archivo

    _auditoria_activa = activa

    if ruta_archivo is None:
        _ruta_archivo = _RUTA_ARCHIVO_PREDETERMINADA
    else:
        _ruta_archivo = Path(ruta_archivo)


def registrar_evento(origen, accion):
    if not _auditoria_activa:
        return False

    try:                                            #se revisa si existe el archivo, de lo contrario se crea.
        if not _ruta_archivo.exists():
            _ruta_archivo.touch()
    except OSError as error:
        raise OSError(
            "Error! El archivo no se pudo abrir con exito."
        ) from error

    try:                                            #se intenta abrir el archivo y en caso de que falle, se tira un error.
        archivo = _ruta_archivo.open("a+", encoding="utf-8")
    except OSError as error:
        raise OSError(
            "Error! El archivo no se pudo abrir con exito."
        ) from error

    fecha_hora = datetime.now().strftime("%d:%m:%Y %H:%M:%S")      #Se obtiene la fecha y hora de la accion
    registro = f"{origen}~{accion}~{fecha_hora}~\n"                #Se formatea el registro de la accion hecha usando '~' como separador

    with archivo:                  #Se busca la linea vacia mas cercana disponible; se escribe al final del archivo.
        archivo.seek(0)
        contenido = archivo.read()
        archivo.seek(0, 2)

        if contenido and not contenido.endswith("\n"):
            archivo.write("\n")

        archivo.write(registro)          #Se escribe en el archivo el registro.

    return True


def leer_registro():
    if not _ruta_archivo.exists():                        #se revisa si existe el archivo, de lo contrario se tira error.
        raise FileNotFoundError(
            "Error! Archivo no encontrado o inexistente."
        )

    try:
        archivo = _ruta_archivo.open("r", encoding="utf-8")            #Se intenta abrir el archivo. Si falla, tira error.
    except OSError as error:
        raise OSError(
            "Error! El archivo no se pudo abrir con exito."
        ) from error

    with archivo:
        lineasTemp = archivo.readlines()                #Se empieza el proceso de leectura.

        if not any(lineaTemp.strip() for lineaTemp in lineasTemp):    #Se revisa si hay siquiera texto. Si el archivo esta vacio, retorna notificacion.
            print("Registro Vacío! No hay datos registrados.")
            return False

        for lineaTemp in lineasTemp:            #Loop de lectura de datos
            if not lineaTemp.strip():
                continue

            datosTemp = lineaTemp.rstrip("\r\n").split("~")

            origenTemp = datosTemp[0]
            accionTemp = datosTemp[1]
            fechaHoraTemp = datosTemp[2]

            print("==============================\n"            #Formato de display de datos.
                  f"Origen: {origenTemp}, Acción: {accionTemp}, Fecha y hora: {fechaHoraTemp}\n"
                  "==============================", end="\n")
            
    return True
