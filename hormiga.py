import random
from tkinter import PhotoImage

class Hormiga:
    def __init__(self, posición_inicial, canvas):
        """
        Inicializa la hormiga con su posición inicial, atributos y carga imágenes para la animación.
        
        :param posición_inicial: Tupla (fila, columna) que define la posición inicial de la hormiga.
        :param canvas: El canvas de Tkinter donde se mostrará la hormiga.
        """
        self.posición = posición_inicial
        self.salud = 100
        self.nivel_alcohol = 0
        self.puntos = 0
        self.secuencia_movimientos = []  # Para almacenar la secuencia de movimientos de la hormiga
        self.anim_frame = 0  # Para alternar entre los dos fotogramas de animación

        # Cargar dos imágenes para cada dirección
        self.imagenes = {
            "arriba": [PhotoImage(file="hormiga/arriba/1.png"), PhotoImage(file="hormiga/arriba/2.png")],
            "abajo": [PhotoImage(file="hormiga/abajo/1.png"), PhotoImage(file="hormiga/abajo/2.png")],
            "izquierda": [PhotoImage(file="hormiga/izquierda/1.png"), PhotoImage(file="hormiga/izquierda/2.png")],
            "derecha": [PhotoImage(file="hormiga/derecha/1.png"), PhotoImage(file="hormiga/derecha/2.png")]
        }
        
        # Canvas y representación de la hormiga en el canvas
        self.canvas = canvas
        self.hormiga_imagen = self.canvas.create_image(
            self.posición[1] * 20, self.posición[0] * 20,  # Asume que cada celda es de 20x20 píxeles
            image=self.imagenes["abajo"][self.anim_frame]
        )

    def mover(self, dirección):
        """
        Mueve la hormiga en una de las cuatro direcciones y actualiza su imagen.
        
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
        
        # Alternar entre las dos imágenes de la dirección actual
        self.anim_frame = (self.anim_frame + 1) % 2
        nueva_imagen = self.imagenes[dirección][self.anim_frame]

        # Actualiza la posición de la imagen en el canvas
        self.canvas.coords(
            self.hormiga_imagen,
            self.posición[1] * 20,  # Columna en el eje X
            self.posición[0] * 20   # Fila en el eje Y
        )
        # Cambia la imagen según la dirección
        self.canvas.itemconfig(self.hormiga_imagen, image=nueva_imagen)
        
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
