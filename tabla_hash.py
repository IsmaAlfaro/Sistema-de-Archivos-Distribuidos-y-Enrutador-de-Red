# Tabla hash manual para credenciales; las colisiones se guardan en listas por índice.
from auditoria import registrar_evento


class TablaHash:

    # Crea tamaño buckets independientes y guarda el servidor para identificar el log.
    # El tamaño previsto es un entero positivo; actualmente no se valida ni redimensiona.
    def __init__(self, tamaño=10, nombre_servidor=None):
        self.tamaño = tamaño
        self.tabla = [[] for _ in range(tamaño)]
        self.nombre_servidor = nombre_servidor

    # Hash polinómico de base 7: cada carácter incorpora el orden de los anteriores.
    # El módulo final limita el índice al arreglo de buckets. El acumulador crece
    # con la longitud del usuario; aplicar módulo en cada paso es una mejora pendiente.
    def funcion_hash(self, usuario):
        suma = 0

        for letra in usuario:
            suma = suma * 7 + ord(letra)

        return suma % self.tamaño

    # Busca duplicados solo en el bucket correspondiente al nombre recibido.
    # Devuelve False si el usuario existe; audita, guarda (usuario, contraseña) y
    # devuelve True si es nuevo. Un error de auditoría interrumpe antes de insertar.
    def registrar_usuario(self, usuario, contraseña):
        indice = self.funcion_hash(usuario)

        for usuario_guardado, contraseña_guardada in self.tabla[indice]:
            if usuario_guardado == usuario:
                return False

        if self.nombre_servidor is None:
            servidorTemp = ""
        else:
            servidorTemp = f" en el servidor '{self.nombre_servidor}'"

        registrar_evento(
            "autenticación",
            f"registro exitoso del usuario '{usuario}'{servidorTemp}"
        )

        self.tabla[indice].append((usuario, contraseña))
        return True

    # Compara las credenciales recibidas con las entradas del bucket calculado.
    # Devuelve True si coinciden o False en otro caso y audita ambos resultados
    # sin incluir la contraseña. Los errores al escribir el log se propagan.
    def autenticar(self, usuario, contraseña):
        indice = self.funcion_hash(usuario)

        if self.nombre_servidor is None:
            servidorTemp = ""
        else:
            servidorTemp = f" en el servidor '{self.nombre_servidor}'"

        for usuario_guardado, contraseña_guardada in self.tabla[indice]:
            if usuario_guardado == usuario and contraseña_guardada == contraseña:
                registrar_evento(
                    "autenticación",
                    f"inicio de sesión exitoso para el usuario "
                    f"'{usuario}'{servidorTemp}"
                )
                return True

        registrar_evento(
            "autenticación",
            f"inicio de sesión fallido para el usuario "
            f"'{usuario}'{servidorTemp}"
        )

        return False
        
