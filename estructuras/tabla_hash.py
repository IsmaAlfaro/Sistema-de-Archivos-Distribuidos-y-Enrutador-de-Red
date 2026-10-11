# Tabla hash manual para credenciales; las colisiones se guardan en listas por índice.
from servicios.auditoria import registrar_evento


class TablaHash:

    # Crea los buckets, valida el tamaño y cuenta los usuarios registrados.
    # La tabla crece cuando supera el factor de carga máximo.
    def __init__(self, tamaño=10, nombre_servidor=None):

        if type (tamaño) is not int or tamaño <= 0:
            raise ValueError("El tamaño de la tabla hash debe ser un entero positivo.")

        self.tamaño = tamaño
        self.tabla = [[] for _ in range(tamaño)]
        self.nombre_servidor = nombre_servidor
        self.cantidad = 0
        self.factor_maximo = 0.75 #Factor de carga máximo permitido antes de redimensionar la tabla hash

    # Hash polinómico de base 7 que considera el orden de los caracteres.
    # Aplica el módulo en cada paso para mantener acotado el acumulador.
    def funcion_hash(self, usuario):
        suma = 0

        for letra in usuario:
            suma = (suma * 7 + ord(letra)) % self.tamaño

        return suma 

    # Busca duplicados solo en el bucket correspondiente al nombre recibido.
    # Devuelve False si el usuario existe; audita, guarda (usuario, contraseña) y
    # devuelve True si es nuevo. Un error de auditoría interrumpe antes de insertar.
    def registrar_usuario(self, usuario, contraseña):
        usuario = usuario.strip()

        if not usuario:
            raise ValueError("El nombre de usuario no puede estar vacío.")

        if not contraseña.strip():
            raise ValueError("La contraseña no puede estar vacía ni contener solo espacios.")

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
        self.cantidad += 1

        factor_actual = self.cantidad / self.tamaño
        if factor_actual > self.factor_maximo:
            self.redimensionar()

        return True

    # Compara las credenciales recibidas con las entradas del bucket calculado.
    # Devuelve True si coinciden o False en otro caso y audita ambos resultados.
    def autenticar(self, usuario, contraseña):
        usuario = usuario.strip()
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
        
    # Duplica las posiciones y redistribuye todas las credenciales.
    # Conserva la cantidad de usuarios y no genera nuevos eventos de registro.
    def redimensionar(self):
        tabla_anterior = self.tabla

        self.tamaño *= 2
        self.tabla = [[] for _ in range(self.tamaño)]

        for lista_usuarios in tabla_anterior:
            for usuario, contraseña in lista_usuarios:
                nuevo_indice = self.funcion_hash(usuario)
                self.tabla[nuevo_indice].append((usuario, contraseña))
