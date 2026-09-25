class TablaHash:

    def __init__(self, tamaño=10):
        self.tamaño = tamaño
        self.tabla = [[] for _ in range(tamaño)]

    def funcion_hash(self, usuario):
        suma = 0

        for letra in usuario:
            suma += ord(letra)

        return suma % self.tamaño

    def registrar_usuario(self, usuario, contraseña):
        indice = self.funcion_hash(usuario)

        for usuario_guardado, contraseña_guardada in self.tabla[indice]:
            if usuario_guardado == usuario:
                return False

        self.tabla[indice].append((usuario, contraseña))
        return True

    def autenticar(self, usuario, contraseña):
        indice = self.funcion_hash(usuario)

        for usuario_guardado, contraseña_guardada in self.tabla[indice]:
            if usuario_guardado == usuario and contraseña_guardada == contraseña:
                return True

        return False