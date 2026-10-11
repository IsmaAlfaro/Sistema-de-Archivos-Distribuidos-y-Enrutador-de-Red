# Registro persistente de eventos y consultas por fecha para todos los módulos.
# Formato actual de cada línea: origen~acción~dd:mm:aaaa HH:MM:SS~
from datetime import datetime
from pathlib import Path


_RUTA_ARCHIVO_PREDETERMINADA = (
    Path(__file__).resolve().parent.parent / "datos" / "network_audit_log.txt"
)
_ruta_archivo = _RUTA_ARCHIVO_PREDETERMINADA
_auditoria_activa = False  # main() la activa; los scripts de prueba parten con ella desactivada.


# Qué hace: activa o desactiva la auditoría y configura dónde se guarda el historial.
# Recibe: activa (booleano) y ruta_archivo (texto, Path o None para usar datos/).
# Devuelve: nada; actualiza la configuración global sin crear el archivo.
def configurar_auditoria(activa, ruta_archivo=None):
    global _auditoria_activa, _ruta_archivo

    _auditoria_activa = activa

    if ruta_archivo is None:
        _ruta_archivo = _RUTA_ARCHIVO_PREDETERMINADA
    else:
        _ruta_archivo = Path(ruta_archivo)


# Qué hace: agrega un evento con la fecha y hora actuales al final del historial.
# Recibe: origen (texto del módulo) y accion (texto que describe lo ocurrido).
# Devuelve: True si escribe el evento o False si la auditoría está desactivada.
# Revisa el último byte para separar registros; lanza OSError si falla la escritura.
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


# Qué hace: quita espacios exteriores y comprueba el formato y la validez de una fecha.
# Recibe: fechaTemp (texto con formato dd:mm:aaaa, por ejemplo 08:10:2026).
# Devuelve: un objeto date; lanza ValueError si el dato o la fecha son inválidos.
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


# Qué hace: lee el historial configurado y omite con un aviso las líneas mal formadas.
# Recibe: ningún parámetro; utiliza la ruta guardada en _ruta_archivo.
# Devuelve: una lista de tuplas (origen, acción, fecha_date, fecha_hora_texto);
# devuelve [] si no hay registros válidos. Lanza FileNotFoundError si falta el archivo
# y propaga los errores de acceso o lectura.
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


# Qué hace: muestra en consola el origen, la acción y la fecha/hora de cada registro.
# Recibe: registrosTemp, una lista de tuplas devuelta por obtenerRegistros.
# Devuelve: nada; únicamente imprime los datos recibidos.
def imprimirRegistros(registrosTemp):
    for registroTemp in registrosTemp:
        origenTemp = registroTemp[0]
        accionTemp = registroTemp[1]
        fechaHoraTemp = registroTemp[3]

        print("==============================\n"
              f"Origen: {origenTemp}, Acción: {accionTemp}, Fecha y hora: {fechaHoraTemp}\n"
              "==============================", end="\n")
        print()


# Qué hace: consulta el archivo de auditoría y muestra todos sus registros válidos.
# Recibe: ningún parámetro; utiliza el historial configurado.
# Devuelve: True si muestra registros o False si no hay registros válidos.
# Propaga los errores de lectura de obtenerRegistros.
def leerRegistro():
    registrosTemp = obtenerRegistros()

    if not registrosTemp:
        print("No hay registros válidos para mostrar.")
        return False

    imprimirRegistros(registrosTemp)
    return True


# Qué hace: muestra los eventos de la fecha indicada en adelante, incluyendo ese día.
# Recibe: fecha (texto con formato dd:mm:aaaa).
# Devuelve: True si muestra coincidencias o False si no encuentra ninguna.
# Propaga los errores de validación de fecha y de lectura del historial.
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


# Qué hace: muestra únicamente los eventos del día indicado, sin importar la hora.
# Recibe: fecha (texto con formato dd:mm:aaaa).
# Devuelve: True si muestra coincidencias o False si no encuentra ninguna.
# Propaga los errores de validación de fecha y de lectura del historial.
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
