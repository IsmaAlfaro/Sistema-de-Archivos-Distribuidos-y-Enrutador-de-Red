# Registro persistente de eventos y consultas por fecha para todos los módulos.
# Formato actual de cada línea: origen~acción~dd:mm:aaaa HH:MM:SS~
from datetime import datetime
from pathlib import Path


_RUTA_ARCHIVO_PREDETERMINADA = Path(__file__).resolve().with_name(
    "network_audit_log.txt"
)
_ruta_archivo = _RUTA_ARCHIVO_PREDETERMINADA
_auditoria_activa = False  # main() la activa; los scripts de prueba parten con ella desactivada.


# Activa/desactiva el registro y permite indicar una ruta alternativa para pruebas.
# Si ruta_archivo es None, restablece la ruta predeterminada junto a este módulo.
# Modifica la configuración global; no crea el archivo ni devuelve datos.
def configurar_auditoria(activa, ruta_archivo=None):
    global _auditoria_activa, _ruta_archivo

    _auditoria_activa = activa

    if ruta_archivo is None:
        _ruta_archivo = _RUTA_ARCHIVO_PREDETERMINADA
    else:
        _ruta_archivo = Path(ruta_archivo)


# Agrega un evento con origen, acción y fecha/hora al final del archivo.
# Devuelve False si la auditoría está desactivada y True después de escribir.
# Revisa únicamente el último byte para evitar unir dos registros.
# Si falla la apertura o escritura, lanza OSError.
def registrar_evento(origen, accion):
    if not _auditoria_activa:
        return False

    fecha_hora = datetime.now().strftime("%d:%m:%Y %H:%M:%S")
    registro = f"{origen}~{accion}~{fecha_hora}~\n"

    try:
        with _ruta_archivo.open("a+b") as archivo:
            # Se posiciona al final para comprobar si el archivo tiene contenido.
            archivo.seek(0, 2)

            if archivo.tell() > 0:
                # Lee solo el último byte del archivo.
                archivo.seek(-1, 2)
                ultimo_byte = archivo.read(1)

                if ultimo_byte != b"\n":
                    archivo.write(b"\n")

            # En modo append, la escritura siempre se agrega al final.
            archivo.write(registro.encode("utf-8"))

    except OSError as error:
        raise OSError(
            "No se pudo guardar el evento en el archivo de auditoría."
        ) from error

    return True


# Recibe texto dd:mm:aaaa, quita espacios exteriores y devuelve un objeto date.
# Lanza ValueError si el tipo, la fecha del calendario o su formato no son válidos.
def validarFecha(fechaTemp):
    if not isinstance(fechaTemp, str):
        raise ValueError("Fecha inválida. Use el formato dd:mm:aaaa.")

    fechaTextoTemp = fechaTemp.strip()

    try:
        fechaConvertidaTemp = datetime.strptime(
            fechaTextoTemp, "%d:%m:%Y"
        ).date()
    except ValueError as error:
        raise ValueError(
            "Fecha inválida. Use el formato dd:mm:aaaa."
        ) from error

    if fechaConvertidaTemp.strftime("%d:%m:%Y") != fechaTextoTemp:
        raise ValueError("Fecha inválida. Use el formato dd:mm:aaaa.")

    return fechaConvertidaTemp


# Lee el log y devuelve tuplas (origen, acción, fecha_date, fecha_hora_texto).
# Un archivo vacío devuelve []; uno inexistente lanza FileNotFoundError.
# Omite registros de formato inválido con un aviso y propaga errores de acceso.
def obtenerRegistros():
    if not _ruta_archivo.exists():
        raise FileNotFoundError(
            "Error! Archivo no encontrado o inexistente."
        )

    try:
        archivo = _ruta_archivo.open("r", encoding="utf-8")
    except OSError as error:
        raise OSError(
            "Error! El archivo no se pudo abrir con exito."
        ) from error

    with archivo:
        lineasTemp = archivo.readlines()  # Carga las líneas antes de cerrar el archivo.

    if not any(lineaTemp.strip() for lineaTemp in lineasTemp):
        return []

    registrosTemp = []

    for numeroLinea, lineaTemp in enumerate(lineasTemp, start=1):
        if not lineaTemp.strip():
            continue

        texto = lineaTemp.rstrip("\r\n")

        try:
            # Cada registro debe terminar con el separador de cierre.
            if not texto.endswith("~"):
                raise ValueError("Falta el separador final.")

            # Retira únicamente el separador de cierre.
            texto = texto[:-1]

            # Separa el origen por la izquierda y la fecha por la derecha.
            # Los separadores intermedios se conservan dentro de la acción.
            origenTemp, resto = texto.split("~", 1)
            accionTemp, fechaHoraTemp = resto.rsplit("~", 1)

            if not origenTemp.strip() or not accionTemp.strip():
                raise ValueError("El origen o la acción están vacíos.")

            fechaRegistroTemp = datetime.strptime(
                fechaHoraTemp, "%d:%m:%Y %H:%M:%S"
            ).date()

        except ValueError:
            print(
                f"Aviso: el registro de la línea {numeroLinea} "
                "tiene un formato inválido y se omitirá."
            )
            continue

        registrosTemp.append(
            (origenTemp, accionTemp, fechaRegistroTemp, fechaHoraTemp)
        )

    return registrosTemp


# Recibe las tuplas de obtenerRegistros y muestra origen, acción y fecha/hora.
# Solo presenta los datos: no consulta el archivo, no filtra y no devuelve resultados.
def imprimirRegistros(registrosTemp):
    for registroTemp in registrosTemp:
        origenTemp = registroTemp[0]
        accionTemp = registroTemp[1]
        fechaHoraTemp = registroTemp[3]

        print("==============================\n"
              f"Origen: {origenTemp}, Acción: {accionTemp}, Fecha y hora: {fechaHoraTemp}\n"
              "==============================", end="\n")
        print()


# Consulta e imprime el historial completo. Devuelve True si mostró registros,
# False si el archivo está vacío y propaga los errores de obtenerRegistros.
def leerRegistro():
    registrosTemp = obtenerRegistros()

    if not registrosTemp:
        print("No hay registros válidos para mostrar.")
        return False

    imprimirRegistros(registrosTemp)
    return True


# Recibe dd:mm:aaaa e imprime registros de esa fecha en adelante (límite inclusivo).
# Devuelve True si hay coincidencias o False si no; propaga errores de fecha/lectura.
def leerRegistroDesde(fecha):
    fechaInicioTemp = validarFecha(fecha)
    registrosTemp = obtenerRegistros()

    if not registrosTemp:
        print("No hay registros válidos para mostrar.")
        return False

    registrosFiltradosTemp = [
        registroTemp
        for registroTemp in registrosTemp
        if registroTemp[2] >= fechaInicioTemp
    ]

    if not registrosFiltradosTemp:
        print("No hay registros desde la fecha indicada.")
        return False

    imprimirRegistros(registrosFiltradosTemp)
    return True


# Recibe dd:mm:aaaa e imprime únicamente los registros del mismo día, sin importar hora.
# Devuelve True si hay coincidencias o False si no; propaga errores de fecha/lectura.
def leerRegistroFecha(fecha):
    fechaEspecificaTemp = validarFecha(fecha)
    registrosTemp = obtenerRegistros()

    if not registrosTemp:
        print("No hay registros válidos para mostrar.")
        return False

    registrosFiltradosTemp = [
        registroTemp
        for registroTemp in registrosTemp
        if registroTemp[2] == fechaEspecificaTemp
    ]

    if not registrosFiltradosTemp:
        print("No hay registros para la fecha indicada.")
        return False

    imprimirRegistros(registrosFiltradosTemp)
    return True
