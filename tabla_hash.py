from auditoria import registrar_evento


class TablaHash:

    def __init__(self, tamaño=10, nombre_servidor=None):
        self.tamaño = tamaño
        self.tabla = [[] for _ in range(tamaño)]
        self.nombre_servidor = nombre_servidor

    def funcion_hash(self, usuario):
        suma = 0

        for letra in usuario:
            suma = suma * 7 + ord(letra)

        return suma % self.tamaño

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
        
