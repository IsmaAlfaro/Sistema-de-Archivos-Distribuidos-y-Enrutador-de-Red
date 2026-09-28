class GrafoRed:

    def __init__(self):#constructor
        self.conexiones = {}#diccionario que almacena las conexiones entre servidores


    def agregar_servidor(self, servidor):#Agrega un servidor al gafro, se le pasa un objeto de la clase servidor
        if servidor.nombre not in self.conexiones:#si no esta agregado
            self.conexiones[servidor.nombre] = {}#lo agrega
            return True

        return False#si ya lo estaba devuelve false


    def agregar_conexion(self, servidor1, servidor2, latencia):#crea conexion entre dos servidores y guarda la latencia, se le pasa self, el nombre de los dos servidores y la latencia
        if servidor1 not in self.conexiones:#si no estan agregados devuelve false
            return False

        if servidor2 not in self.conexiones:
            return False

        if servidor1 == servidor2:#si son iguales devuelve false
            return False

        if latencia <= 0:#rechazamos latencias negativas o cero
            return False

        #guarda la conexion en ambos sentidos, ya que es un grafo no dirigido
        self.conexiones[servidor1][servidor2] = latencia
        self.conexiones[servidor2][servidor1] = latencia

        return True


    def eliminar_conexion(self, servidor1, servidor2):
        if servidor1 not in self.conexiones:#si no estan agregados devuelve false
            return False

        if servidor2 not in self.conexiones:
            return False

        if servidor2 not in self.conexiones[servidor1]:#si el servidor 2 no esta conectado al servidor 1 devuelve false
            return False

        del self.conexiones[servidor1][servidor2]#Se eliminan las conexiones con la funcion de python del
        del self.conexiones[servidor2][servidor1]

        return True


    def mostrar_red(self):
        for servidor in self.conexiones:#por cada servidor que hay
            print(servidor)#imprime el nombre del servidor

            for vecino, latencia in self.conexiones[servidor].items():#por cada vecino que tiene el sevidor
                print("  ->", vecino, "-", latencia, "ms")#imprime el nombre del vecino y la latencia