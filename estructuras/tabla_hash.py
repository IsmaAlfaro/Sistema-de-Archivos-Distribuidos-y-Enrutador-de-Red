# Tabla hash manual para credenciales; las colisiones se guardan en listas por índice.
from servicios.auditoria import registrar_evento


class TablaHash:

    # Qué hace: crea las listas de usuarios e inicia el contador y el límite de carga.
    # Recibe: tamaño (entero positivo, 10 por defecto) y nombre_servidor (texto o None).
    # Devuelve: nada; inicializa la tabla. Lanza ValueError si el tamaño es inválido.
    def __init__(self, tamaño=10, nombre_servidor=None):

        if type (tamaño) is not int or tamaño <= 0:
            raise ValueError("El tamaño de la tabla hash debe ser un entero positivo.")

        self.tamaño = tamaño
        self.tabla = [[] for _ in range(tamaño)]
        self.nombre_servidor = nombre_servidor
        self.cantidad = 0
        self.factor_maximo = 0.75 #Factor de carga máximo permitido antes de redimensionar la tabla hash

    # Qué hace: calcula la posición del usuario con un hash de base 7 y módulo por paso.
    # Recibe: usuario (texto), cuyo orden de caracteres influye en el cálculo.
    # Devuelve: un índice entero entre 0 y tamaño - 1.
    def funcion_hash(self, usuario):
        suma = 0

        for letra in usuario:
            suma = (suma * 7 + ord(letra)) % self.tamaño

        return suma 

    # Qué hace: quita espacios exteriores del usuario, valida las credenciales,
    # audita el registro y las guarda; amplía la tabla si supera el límite de carga.
    # Recibe: usuario y contraseña (textos); conserva los espacios de la contraseña.
    # Devuelve: True si registra al usuario o False si ese nombre ya existe.
    # Lanza ValueError por credenciales vacías y OSError si falla la auditoría.
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

    # Qué hace: busca al usuario, compara la contraseña exacta y audita el resultado.
    # Recibe: usuario y contraseña (textos); quita espacios exteriores del usuario.
    # Devuelve: True si las credenciales coinciden o False en caso contrario.
    # Si falla la auditoría, lanza OSError.
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
        
    # Qué hace: duplica la capacidad y recalcula la posición de todas las credenciales.
    # Recibe: ningún dato adicional; utiliza el tamaño y los usuarios de esta tabla.
    # Devuelve: nada; actualiza la tabla conservando usuarios, contraseñas y contador.
    # No genera nuevos eventos de registro en auditoría.
    def redimensionar(self):
        tabla_anterior = self.tabla

        self.tamaño *= 2
        self.tabla = [[] for _ in range(self.tamaño)]

        for lista_usuarios in tabla_anterior:
            for usuario, contraseña in lista_usuarios:
                nuevo_indice = self.funcion_hash(usuario)
                self.tabla[nuevo_indice].append((usuario, contraseña))
