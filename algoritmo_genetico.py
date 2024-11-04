import random

# Acciones posibles como alelos: mover en una dirección o comer
ACTIONS = ["arriba", "abajo", "izquierda", "derecha", "comer"]

class AlgoritmoGenetico:
    def __init__(self, tamaño_poblacion=20, tasa_mutacion=0.1, generaciones=50):
        """
        Inicializa el algoritmo genético con parámetros básicos.

        :param tamaño_poblacion: Cantidad de secuencias en cada generación.
        :param tasa_mutacion: Probabilidad de mutación en cada alelo.
        :param generaciones: Número de generaciones para evolucionar.
        """
        self.tamaño_poblacion = tamaño_poblacion
        self.tasa_mutacion = tasa_mutacion
        self.generaciones = generaciones
        self.poblacion = self.inicializar_poblacion()

    def inicializar_poblacion(self):
        """
        Genera una población inicial aleatoria de secuencias de movimientos.

        :return: Lista de secuencias de movimientos (población inicial).
        """
        return [[random.choice(ACTIONS) for _ in range(10)] for _ in range(self.tamaño_poblacion)]

    def evaluar_fitness(self, secuencia, laberinto, hormiga):
        """
        Evalúa la secuencia en función de los puntos obtenidos por la hormiga.

        :param secuencia: Secuencia de movimientos a evaluar.
        :param laberinto: Instancia del laberinto donde se realiza la simulación.
        :param hormiga: Instancia de la hormiga que ejecutará la secuencia.
        :return: Puntuación obtenida (fitness).
        """
        hormiga.reiniciar()  # Resetea la hormiga para evaluar cada secuencia desde el inicio
        for accion in secuencia:
            if hormiga.salud <= 0:
                break  # Detiene si la hormiga muere
            if accion in ["arriba", "abajo", "izquierda", "derecha"]:
                hormiga.mover(accion)
            elif accion == "comer":
                hormiga.comer(laberinto.matriz[hormiga.posición[0]][hormiga.posición[1]])
        return hormiga.puntos  # Fitness basado en puntos obtenidos

    def seleccionar(self):
        """
        Selecciona las mejores secuencias de la población actual para reproducir.

        :return: Lista de las secuencias seleccionadas.
        """
        self.poblacion.sort(key=lambda x: x[1], reverse=True)  # Ordena por puntuación (fitness)
        return [secuencia for secuencia, _ in self.poblacion[:self.tamaño_poblacion // 2]]  # Selección elitista

    def cruzar(self, padre1, padre2):
        """
        Realiza el cruzamiento entre dos secuencias de movimientos.

        :param padre1: Secuencia de movimientos de un padre.
        :param padre2: Secuencia de movimientos del otro padre.
        :return: Dos nuevas secuencias resultantes del cruzamiento.
        """
        punto_corte = random.randint(1, len(padre1) - 2)
        hijo1 = padre1[:punto_corte] + padre2[punto_corte:]
        hijo2 = padre2[:punto_corte] + padre1[punto_corte:]
        return hijo1, hijo2

    def mutar(self, secuencia):
        """
        Realiza mutaciones en una secuencia de movimientos con una probabilidad definida.

        :param secuencia: Secuencia de movimientos a mutar.
        :return: Secuencia de movimientos mutada.
        """
        return [random.choice(ACTIONS) if random.random() < self.tasa_mutacion else accion for accion in secuencia]

    def evolucionar(self, laberinto, hormiga):
        """
        Ejecuta el ciclo de generaciones para evolucionar las secuencias de movimientos.

        :param laberinto: Instancia del laberinto.
        :param hormiga: Instancia de la hormiga.
        :return: La mejor secuencia obtenida después de las generaciones.
        """
        for _ in range(self.generaciones):
            # Evaluación de fitness
            self.poblacion = [(secuencia, self.evaluar_fitness(secuencia, laberinto, hormiga)) for secuencia in self.poblacion]
            
            # Selección
            seleccionados = self.seleccionar()
            
            # Cruzamiento y creación de la nueva generación
            nueva_poblacion = []
            while len(nueva_poblacion) < self.tamaño_poblacion:
                padre1, padre2 = random.sample(seleccionados, 2)
                hijo1, hijo2 = self.cruzar(padre1, padre2)
                nueva_poblacion.extend([self.mutar(hijo1), self.mutar(hijo2)])
            
            # Actualización de la población
            self.poblacion = nueva_poblacion[:self.tamaño_poblacion]
        
        # Selección final del mejor individuo
        mejor_secuencia = max(self.poblacion, key=lambda x: self.evaluar_fitness(x, laberinto, hormiga))
        return mejor_secuencia
