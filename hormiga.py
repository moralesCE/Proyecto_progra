#hormiga.py
from PIL import Image, ImageTk
from vino import Vino

class Hormiga:
    def __init__(self, posición_inicial, canvas, app, cell_size=50):
        self.posición_inicial = posición_inicial
        self.posición = posición_inicial
        self.canvas = canvas
        self.cell_size = cell_size  # Tamaño de cada celda
        self.salud = 100
        self.nivel_alcohol = 0
        self.puntos = 0
        self.secuencia_movimientos = []
        self.anim_frame = 0
        self.dirección_actual = "abajo"
        self.movimiento_pendiente = False  # Flag to avoid overlapping animations
        self.app = app  # Reference to LaberintoApp to update points on GUI
        
        # Cargar imágenes para la animación de la hormiga en cada dirección
        self.imagenes = {
            "arriba": [
                ImageTk.PhotoImage(Image.open("hormiga/arriba/1.png")),
                ImageTk.PhotoImage(Image.open("hormiga/arriba/2.png"))
            ],
            "abajo": [
                ImageTk.PhotoImage(Image.open("hormiga/abajo/1.png")),
                ImageTk.PhotoImage(Image.open("hormiga/abajo/2.png"))
            ],
            "izquierda": [
                ImageTk.PhotoImage(Image.open("hormiga/izquierda/1.png")),
                ImageTk.PhotoImage(Image.open("hormiga/izquierda/2.png"))
            ],
            "derecha": [
                ImageTk.PhotoImage(Image.open("hormiga/derecha/1.png")),
                ImageTk.PhotoImage(Image.open("hormiga/derecha/2.png"))
            ]
        }
        
        # Inicializa la imagen de la hormiga en el canvas
        x_centro = self.posición[1] * self.cell_size + self.cell_size // 2
        y_centro = self.posición[0] * self.cell_size + self.cell_size // 2
        self.hormiga_imagen = self.canvas.create_image(
            x_centro, y_centro,
            image=self.imagenes[self.dirección_actual][self.anim_frame]
        )

    def mover(self, direccion, laberinto):
        """Moves the ant in the given direction and consumes items if present."""
        if self.movimiento_pendiente:
            return  # Skip if movement is already in progress

        if not isinstance(direccion, str) or direccion not in ["arriba", "abajo", "izquierda", "derecha"]:
            print(f"Error: 'direccion' should be a string ('arriba', 'abajo', 'izquierda', 'derecha'), got: {direccion}")
            return

        nueva_fila, nueva_columna = self.posición
        if direccion == "arriba":
            nueva_fila -= 1
        elif direccion == "abajo":
            nueva_fila += 1
        elif direccion == "izquierda":
            nueva_columna -= 1
        elif direccion == "derecha":
            nueva_columna += 1

        filas, columnas = laberinto.tamaño
        if 0 <= nueva_fila < filas and 0 <= nueva_columna < columnas and laberinto.matriz[nueva_fila][nueva_columna] != 1:
            # Move the ant to the new position and animate movement
            self.posición = (nueva_fila, nueva_columna)
            x_target = nueva_columna * self.cell_size + self.cell_size // 2
            y_target = nueva_fila * self.cell_size + self.cell_size // 2
            self.movimiento_pendiente = True
            self.animar_movimiento(x_target, y_target, direccion)

            # Check for items to consume at the new position
            item_value = laberinto.matriz[nueva_fila][nueva_columna]
            if item_value == 2:  # azucar
                self.comer("azúcar", (nueva_fila, nueva_columna))
            elif item_value == 3:  # veneno
                self.comer("veneno", (nueva_fila, nueva_columna))
            elif item_value == 4:  # vino
                self.comer("vino", (nueva_fila, nueva_columna))


    def animar_movimiento(self, x_target, y_target, direccion):
        """Animate the ant's movement toward the target position smoothly."""
        # Ensure direccion is a string
        if isinstance(direccion, list):
            print(f"Error: 'direccion' should be a string, got a list: {direccion}")
            direccion = direccion[0] if direccion else "abajo"  # Default to "abajo"

        x_current, y_current = self.canvas.coords(self.hormiga_imagen)

        if abs(x_target - x_current) > 1 or abs(y_target - y_current) > 1:
            step_x = (x_target - x_current) / 5
            step_y = (y_target - y_current) / 5
            self.canvas.move(self.hormiga_imagen, step_x, step_y)
            self.canvas.after(30, self.animar_movimiento, x_target, y_target, direccion)
        else:
            # Snap to final position
            self.canvas.coords(self.hormiga_imagen, x_target, y_target)
            self.movimiento_pendiente = False

            # Update animation frame
            self.anim_frame = (self.anim_frame + 1) % len(self.imagenes[direccion])
            self.canvas.itemconfig(self.hormiga_imagen, image=self.imagenes[direccion][self.anim_frame])



    def actualizar_animacion(self):
        """
        Actualiza el fotograma de la hormiga para simular movimiento continuo en la dirección actual.
        Este método alterna entre los fotogramas de la dirección actual.
        """
        self.anim_frame = (self.anim_frame + 1) % len(self.imagenes[self.dirección_actual])
        self.canvas.itemconfig(self.hormiga_imagen, image=self.imagenes[self.dirección_actual][self.anim_frame])


    def reiniciar(self):
        """Restaura la hormiga a su estado inicial."""
        self.posición = self.posición_inicial
        self.salud = 100
        self.nivel_alcohol = 0
        self.puntos = 0
        self.secuencia_movimientos = []
        self.anim_frame = 0
        self.dirección_actual = "abajo"
        # Mueve la imagen de la hormiga al inicio
        x_centro = self.posición[1] * self.cell_size + self.cell_size // 2
        y_centro = self.posición[0] * self.cell_size + self.cell_size // 2
        self.canvas.coords(self.hormiga_imagen, x_centro, y_centro)
        self.canvas.itemconfig(self.hormiga_imagen, image=self.imagenes[self.dirección_actual][self.anim_frame])

    def comer(self, item, item_coords=None):
        """Consumes an item and updates points and health based on item type."""
        if item == "azúcar":
            self.puntos += 10
            self.salud = min(100, self.salud + 5)
            print("Hormiga comió azúcar. Salud incrementada y puntos ganados.")
            self.app.actualizar_puntos(self.puntos)
            
            # Remove azucar from canvas and matrix
            if item_coords:
                fila, columna = item_coords
                self.canvas.delete(self.app.placed_images[(fila, columna)])  # Remove from canvas
                del self.app.placed_images[(fila, columna)]  # Remove from placed images reference
                self.app.laberinto.matriz[fila][columna] = 0  # Clear the matrix cell

        elif item == "vino" and item_coords:
            vino = Vino()
            self.modificar_nivel_alcohol(vino.incremento_alcohol)
            self.salud = max(0, self.salud - 10)
            print("Hormiga bebió vino. Salud reducida y nivel de alcohol incrementado.")
            
            # Remove vino from canvas and matrix
            fila, columna = item_coords
            self.canvas.delete(self.app.placed_images[(fila, columna)])
            del self.app.placed_images[(fila, columna)]
            self.app.laberinto.matriz[fila][columna] = 0
            self.app.laberinto.ítems["vino"] = [(f, c, v) for f, c, v in self.app.laberinto.ítems["vino"]
                                                if (f, c) != (fila, columna)]

        elif item == "veneno" and item_coords:
            # "Kill" the ant by setting its health to 0 and removing it from canvas
            self.salud = 0
            print("Hormiga comió veneno. Creando nueva hormiga en la misma posición.")
            
            # Notify the LaberintoApp to create a new Hormiga in the same position
            self.app.crear_nueva_hormiga(self.posición)

            # Remove veneno from canvas and matrix
            fila, columna = item_coords
            self.canvas.delete(self.app.placed_images[(fila, columna)])
            del self.app.placed_images[(fila, columna)]
            self.app.laberinto.matriz[fila][columna] = 0
            self.app.laberinto.ítems["veneno"] = [(f, c, v) for f, c, v in self.app.laberinto.ítems["veneno"]
                                                if (f, c) != (fila, columna)]

        if self.salud <= 0:
            self.canvas.delete(self.hormiga_imagen)  # Remove dead ant image from canvas

    def modificar_nivel_alcohol(self, incremento):
        """
        Increases the level of alcohol by a specified amount.
        
        :param incremento: Amount to increase the alcohol level.
        """
        self.nivel_alcohol += incremento
        print(f"Nivel de alcohol de la hormiga incrementado en {incremento}. Nivel actual: {self.nivel_alcohol}")
        # Optional: Add logic here to handle any effects of increased alcohol level.

