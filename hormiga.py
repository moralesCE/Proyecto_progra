import random

class Hormiga:
    def __init__(self, posición_inicial):
        """
        Inicializa la hormiga con su posición inicial y sus atributos de salud, nivel de alcohol y puntos.
        
        :param posición_inicial: Tupla (fila, columna) que define la posición inicial de la hormiga.
        """
        self.posición = posición_inicial
        self.salud = 100
        self.nivel_alcohol = 0
        self.puntos = 0
        self.secuencia_movimientos = []  # Para almacenar la secuencia de movimientos de la hormiga

    def mover(self, dirección):
        """
        Mueve la hormiga en una de las cuatro direcciones: 'arriba', 'abajo', 'izquierda', 'derecha'.
        
        :param dirección: Dirección en la que se desea mover la hormiga.
        """
        if dirección == "arriba":
            self.posición = (self.posición[0] - 1, self.posición[1])
        elif dirección == "abajo":
            self.posición = (self.posición[0] + 1, self.posición[1])
        elif dirección == "izquierda":
            self.posición = (self.posición[0], self.posición[1] - 1)
        elif dirección == "derecha":
            self.posición = (self.posición[0], self.posición[1] + 1)
        # Agrega el movimiento a la secuencia
        self.secuencia_movimientos.append(dirección)

    def comer(self, ítem):
        """
        Interactúa con el ítem encontrado en la celda. Modifica los atributos según el ítem.
        
        :param ítem: Tipo de ítem encontrado ('azúcar', 'vino', 'veneno').
        """
        if ítem == "azúcar":
            self.puntos += 10
        elif ítem == "vino":
            self.modificar_nivel_alcohol(10)
        elif ítem == "veneno":
            self.modificar_salud(-100)  # Veneno reduce la salud a 0, matando a la hormiga
        # Agrega el ítem consumido a la secuencia
        self.secuencia_movimientos.append("comer")

    def modificar_salud(self, cambio):
        """
        Ajusta el nivel de salud de la hormiga según el cambio indicado.
        
        :param cambio: Cantidad en la que se modifica la salud (puede ser positivo o negativo).
        """
        self.salud = max(0, min(self.salud + cambio, 100))  # Salud entre 0 y 100

    def modificar_nivel_alcohol(self, cambio):
        """
        Ajusta el nivel de alcohol de la hormiga según el cambio indicado.
        
        :param cambio: Cantidad en la que se modifica el nivel de alcohol (puede ser positivo o negativo).
        """
        self.nivel_alcohol = max(0, min(self.nivel_alcohol + cambio, 50))  # Nivel de alcohol entre 0 y 50

    def algoritmo_genético(self):
        """
        Define una secuencia de movimientos para la hormiga, que puede mutar en cada generación.
        Genera una secuencia aleatoria como ejemplo inicial.
        """
        acciones = ["arriba", "abajo", "izquierda", "derecha", "comer"]
        self.secuencia_movimientos = [random.choice(acciones) for _ in range(10)]  # Ejemplo de secuencia de 10 pasos

    def __str__(self):
        """
        Representación en cadena de la hormiga, para visualizar sus atributos y estado actual.
        """
        return (f"Hormiga en posición {self.posición} | Salud: {self.salud} | "
                f"Nivel de Alcohol: {self.nivel_alcohol} | Puntos: {self.puntos}")
