# laberinto.py
from collections import deque
class Laberinto:
    def __init__(self, tamaño):
        """
        Inicializa el laberinto con una matriz de tamaño personalizado, llena de 0s.
        
        :param tamaño: Tupla (filas, columnas) que define el tamaño del laberinto.
        """
        self.tamaño = tamaño  # Define el tamaño como atributo de la clase
        self.meta_posición = None  # No tiene una posición de meta predeterminada
        filas, columnas = tamaño
        # Inicializa la matriz del laberinto con 0s
        self.matriz = [[0 for _ in range(columnas)] for _ in range(filas)]
        self.ítems = {
            "azúcar": [],
            "vino": [],
            "veneno": [],
            "roca": []
        }

    def crear_laberinto(self):
        """
        Este método ahora no colocará ítems iniciales. 
        La matriz se deja como 0s y solo cambiará si se coloca un ítem.
        """
        pass  # No se realiza ninguna modificación inicial en la matriz

    def actualizar_estado(self, posición, nuevo_estado):
        """
        Actualiza el contenido de una casilla en el laberinto a medida que la hormiga avanza.
        
        :param posición: Tupla (fila, columna) de la posición a actualizar.
        :param nuevo_estado: Estado nuevo que se asignará a la casilla.
        """
        fila, columna = posición
        if 0 <= fila < self.tamaño[0] and 0 <= columna < self.tamaño[1]:
            self.matriz[fila][columna] = nuevo_estado

    def mostrar_laberinto(self):
        """
        Muestra el estado actual del laberinto, útil para depuración o visualización.
        """
        for fila in self.matriz:
            print(" ".join(str(celda) for celda in fila))
        print("\n")

    def establecer_meta(self, fila, columna):
        """
        Coloca la meta en una posición específica de la matriz.
        
        :param fila: Fila donde se colocará la meta.
        :param columna: Columna donde se colocará la meta.
        """
        # Elimina la meta anterior si existía
        if self.meta_posición:
            anterior_fila, anterior_columna = self.meta_posición
            self.matriz[anterior_fila][anterior_columna] = 0  # Limpia la posición anterior

        # Establece la nueva posición de la meta
        self.matriz[fila][columna] = 5  # Representa la meta con el número 5
        self.meta_posición = (fila, columna)  # Guarda la nueva posición de la meta


    def verificar_meta_accesible(self):
        """Verifies if the goal ('meta') is reachable from any accessible cell in the maze."""
        # Return True if meta has not been placed
        if not self.meta_posición:
            return True

        # Initialize BFS from any open cell
        start_position = None
        for i in range(self.tamaño[0]):
            for j in range(self.tamaño[1]):
                if self.matriz[i][j] == 0:  # Find an empty cell to start the search
                    start_position = (i, j)
                    break
            if start_position:
                break

        if not start_position:
            print("No hay celdas vacías desde las que iniciar la búsqueda.")
            return False

        # Perform BFS to find path to `meta`
        fila_meta, columna_meta = self.meta_posición
        queue = deque([start_position])
        visited = set()
        visited.add(start_position)

        while queue:
            fila, columna = queue.popleft()

            if (fila, columna) == (fila_meta, columna_meta):
                return True  # Path found to the meta

            # Explore neighbors
            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                fila_vecina, columna_vecina = fila + dx, columna + dy
                if (
                    0 <= fila_vecina < self.tamaño[0] and
                    0 <= columna_vecina < self.tamaño[1] and
                    self.matriz[fila_vecina][columna_vecina] != 1 and  # Not a rock
                    (fila_vecina, columna_vecina) not in visited
                ):
                    queue.append((fila_vecina, columna_vecina))
                    visited.add((fila_vecina, columna_vecina))

        print("Meta no es accesible desde ninguna celda abierta.")
        return False  # No path to meta
