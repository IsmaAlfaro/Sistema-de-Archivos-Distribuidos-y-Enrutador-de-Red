# Implementación alternativa basada en diccionarios; main usa grafo_red.py.
# Aquí cada nombre se asocia a un diccionario {nombre_vecino: latencia}.
class GrafoRed:

    # Inicializa una red vacía; esta versión conserva nombres, no objetos Servidor.
    def __init__(self):
        self.conexiones = {}


    # Recibe un Servidor y agrega su nombre sin vecinos. Devuelve True si es nuevo
    # o False si ya existe; no genera eventos de auditoría.
    def agregar_servidor(self, servidor):
        if servidor.nombre not in self.conexiones:
            self.conexiones[servidor.nombre] = {}
            return True

        return False


    # Recibe dos nombres y una latencia numérica; crea o actualiza el enlace bidireccional.
    # Devuelve False si falta un extremo, son iguales o latencia <= 0; True al guardar.
    # A diferencia de grafo_red.py, un enlace existente se sobrescribe en esta versión.
    def agregar_conexion(self, servidor1, servidor2, latencia):
        if servidor1 not in self.conexiones:
            return False

        if servidor2 not in self.conexiones:
            return False

        if servidor1 == servidor2:#si son iguales devuelve false
            return False

        if latencia <= 0:
            return False

        # El grafo es no dirigido: ambos extremos guardan el mismo peso.
        self.conexiones[servidor1][servidor2] = latencia
        self.conexiones[servidor2][servidor1] = latencia

        return True


    # Recibe dos nombres y quita el enlace en ambos extremos, conservando sus vértices.
    # Devuelve True si lo eliminó o False si falta un servidor o la conexión.
    def eliminar_conexion(self, servidor1, servidor2):
        if servidor1 not in self.conexiones:
            return False

        if servidor2 not in self.conexiones:
            return False

        if servidor2 not in self.conexiones[servidor1]:
            return False

        del self.conexiones[servidor1][servidor2]
        del self.conexiones[servidor2][servidor1]

        return True


    # Imprime cada servidor y sus vecinos con latencia en ms; no devuelve datos.
    # Cada enlace aparecerá dos veces, una desde cada extremo.
    def mostrar_red(self):
        for servidor in self.conexiones:
            print(servidor)

            for vecino, latencia in self.conexiones[servidor].items():
                print("  ->", vecino, "-", latencia, "ms")
