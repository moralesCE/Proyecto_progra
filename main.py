#main.py
import tkinter as tk
import functools
from tkinter import messagebox, simpledialog
from PIL import Image, ImageTk
from laberinto import Laberinto
from hormiga import Hormiga
from azucar import Azucar
from vino import Vino
from veneno import Veneno
from algoritmo_genetico import AlgoritmoGenetico
import random

class LaberintoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Simulación de la Hormiga - Configuración del Laberinto")
        
        # Variables de configuración
        self.tamaño = (5, 5)  # Tamaño inicial del laberinto
        self.laberinto = None  # Se creará después de definir el tamaño
        self.posición_hormiga = None  # Posición inicial de la hormiga
        self.hormiga = None
        self.algoritmo_genetico = AlgoritmoGenetico()  # Instancia del algoritmo genético
        self.cell_size = 50  # Tamaño constante de cada celda en píxeles
        self.selected_item = None  # Ítem seleccionado para colocar en el laberinto
        self.puntos = 0  # Initialize points variable to track points
        self.hormiga = None  # Initialize without an ant

        
        
        # Almacenamiento de referencias de imágenes para evitar que se eliminen
        self.placed_images = {}
        
        # Configuración de la interfaz
        self.configurar_interfaz()
        
    def configurar_interfaz(self):
        # Control panel for main buttons and points display
        control_frame = tk.Frame(self.root)
        control_frame.pack(pady=10)

        # Points display label
        self.points_label = tk.Label(control_frame, text=f"Puntos: {self.puntos}", font=("Helvetica", 14))
        self.points_label.grid(row=0, column=0, padx=5)

        # Botón para elegir el tamaño del laberinto
        btn_tamaño = tk.Button(control_frame, text="Elegir Tamaño del Laberinto", command=self.elegir_tamaño)
        btn_tamaño.grid(row=0, column=1, padx=5)
        
        # Botón para iniciar la simulación
        btn_iniciar = tk.Button(control_frame, text="Iniciar Simulación", command=self.iniciar_movimiento_aleatorio)
        btn_iniciar.grid(row=0, column=2, padx=5)

        # Botón para limpiar el canvas
        btn_limpiar = tk.Button(control_frame, text="Limpiar Canvas", command=self.limpiar_canvas)
        btn_limpiar.grid(row=0, column=3, padx=5)

        # Toolbar for selecting icons
        self.toolbar = tk.Frame(self.root)
        self.toolbar.pack(side="left", padx=10, pady=10, fill="y")

        # Cargar imágenes de íconos para la barra de herramientas sin redimensionar
        self.icons = {
            "hormiga": tk.PhotoImage(file="icons/hormiga.png"),
            "azúcar": ImageTk.PhotoImage(Image.open("icons/azucar.png").resize((20, 25))),
            "vino": ImageTk.PhotoImage(Image.open("icons/vino.png").resize((20, 25))),  
            "veneno": ImageTk.PhotoImage(Image.open("icons/veneno.png").resize((20, 25))), 
            "roca": ImageTk.PhotoImage(Image.open("icons/roca.png").resize((26, 26))),
            "meta": ImageTk.PhotoImage(Image.open("icons/meta.png").resize((26, 26)))
        }

        # Crear botones en la barra de herramientas para seleccionar elementos
        for item, icon in self.icons.items():
            btn = tk.Button(self.toolbar, image=icon, command=lambda i=item: self.seleccionar_item(i))
            btn.pack(pady=5)

        # Canvas container for maze
        self.laberinto_canvas = tk.Canvas(self.root)
        self.laberinto_canvas.pack(padx=10, pady=10)

        # Initialize maze with default size
        self.crear_laberinto()

    def actualizar_puntos(self, puntos):
        """Update the points display on the GUI."""
        self.puntos = puntos
        self.points_label.config(text=f"Puntos: {self.puntos}")
        
    def seleccionar_item(self, item):
        """Selecciona un ítem para colocar en el laberinto."""
        self.selected_item = item
        print(f"Elemento seleccionado: {self.selected_item}")

    def elegir_tamaño(self):
        # Diálogo para obtener el tamaño del laberinto
        filas = simpledialog.askinteger("Filas", "Número de filas (min 3, max 10):", minvalue=3, maxvalue=10)
        columnas = simpledialog.askinteger("Columnas", "Número de columnas (min 3, max 10):", minvalue=3, maxvalue=10)
        
        if filas and columnas:
            self.tamaño = (filas, columnas)
            self.crear_laberinto()
        
    def crear_laberinto(self):
       # Limpia el canvas y crea una nueva instancia de laberinto
        self.laberinto_canvas.delete("all")
        
        # Re-crea el laberinto con el tamaño especificado
        self.laberinto = Laberinto(self.tamaño)  # Crea una nueva instancia con el tamaño deseado
        self.laberinto.crear_laberinto()  # Llama a crear_laberinto del objeto Laberinto
        self.laberinto.mostrar_laberinto()  # Muestra el laberinto en consola
        
        # Calcula el tamaño total del canvas basado en el tamaño de cada celda y el tamaño del laberinto
        filas, columnas = self.laberinto.tamaño
        canvas_width = self.cell_size * columnas
        canvas_height = self.cell_size * filas
        
        # Ajusta el tamaño del canvas de acuerdo al tamaño del laberinto
        self.laberinto_canvas.config(width=canvas_width, height=canvas_height)
        
        # Dibuja el laberinto en el canvas con celdas de tamaño constante
        for i in range(filas):
            for j in range(columnas):
                x1 = j * self.cell_size
                y1 = i * self.cell_size
                x2 = x1 + self.cell_size
                y2 = y1 + self.cell_size
                # Crea un rectángulo para cada celda
                rect = self.laberinto_canvas.create_rectangle(x1, y1, x2, y2, fill="white", outline="black", tags="cell")
                # Añade un binding al rectángulo para editar la celda, usando functools.partial para pasar i y j
                self.laberinto_canvas.tag_bind(rect, "<Button-1>", functools.partial(self.colocar_item, i, j))

    def colocar_item(self, fila, columna, event=None):
        """Coloca el ítem seleccionado en la posición del canvas, actualizando la matriz y reemplazando objetos."""
        if not self.selected_item:
            messagebox.showwarning("Advertencia", "Seleccione un ítem antes de colocarlo.")
            return

        # 1. Limpia la celda si ya tiene un ítem
        if (fila, columna) in self.placed_images:
            print(f"Eliminando imagen existente en ({fila}, {columna})")
            self.laberinto_canvas.delete(self.placed_images[(fila, columna)])
            del self.placed_images[(fila, columna)]
            self.laberinto.matriz[fila][columna] = None  # Limpia el valor en la matriz
        else:
            print(f"No hay imagen previa en ({fila}, {columna}) para eliminar.")

        # 2. Dependiendo del ítem seleccionado, actualizamos el Canvas y la matriz con el nuevo objeto
        if self.selected_item == "hormiga":
            # Elimina la hormiga anterior si existe
            if self.hormiga:
                print("Eliminando hormiga previa")
                self.laberinto_canvas.delete(self.hormiga.hormiga_imagen)
                # Limpia la posición anterior de la hormiga en la matriz
                if self.posición_hormiga:
                    fila_anterior, columna_anterior = self.posición_hormiga
                    self.laberinto.matriz[fila_anterior][columna_anterior] = None

            # Crea la nueva hormiga y actualiza la matriz
            self.hormiga = Hormiga((fila, columna), self.laberinto_canvas, self)  # Pass self as the app argument
            self.laberinto.matriz[fila][columna] = 6  # Valor 6 para la hormiga en la matriz
            
            # Calcula la posición centrada en la celda
            x = columna * self.cell_size + self.cell_size // 2
            y = fila * self.cell_size + self.cell_size // 2

            # Coloca la imagen de la hormiga centrada en la celda
            if hasattr(self.hormiga, 'hormiga_imagen') and self.hormiga.hormiga_imagen:
                # Si ya existe una imagen, solo mueve la hormiga
                print("Moviendo hormiga existente a la nueva posición")
                self.laberinto_canvas.coords(self.hormiga.hormiga_imagen, x, y)
            else:
                # Si es la primera vez, crea la imagen de la hormiga en el canvas
                print("Creando nueva imagen de hormiga en el canvas")
                image_id = self.laberinto_canvas.create_image(
                    x, y,
                    image=self.hormiga.imagenes[self.hormiga.dirección_actual][self.hormiga.anim_frame]
                )
                # Almacena la referencia de la imagen en la hormiga
                self.hormiga.hormiga_imagen = image_id

            # Actualiza la posición actual de la hormiga
            self.posición_hormiga = (fila, columna)
            self.placed_images[(fila, columna)] = self.hormiga.hormiga_imagen  # Actualiza la referencia en placed_images

        elif self.selected_item == "azúcar":
            # Place the sugar object in the maze and canvas
            azucar_obj = Azucar()
            self.laberinto.matriz[fila][columna] = 2  # Represent sugar with value 2 in the matrix
            x = columna * self.cell_size + self.cell_size // 2
            y = fila * self.cell_size + self.cell_size // 2
            image_id = self.laberinto_canvas.create_image(x, y, image=azucar_obj.imagen)
            self.placed_images[(fila, columna)] = image_id
            self.laberinto.ítems["azúcar"].append((fila, columna, azucar_obj))  # Track sugar object

        if self.selected_item == "vino":
            # Place the wine object in the maze and canvas
            vino_obj = Vino()
            self.laberinto.matriz[fila][columna] = 4  # Represent wine with value 4 in the matrix
            x = columna * self.cell_size + self.cell_size // 2
            y = fila * self.cell_size + self.cell_size // 2
            image_id = self.laberinto_canvas.create_image(x, y, image=self.icons["vino"])
            self.placed_images[(fila, columna)] = image_id
            self.laberinto.ítems["vino"].append((fila, columna, vino_obj))  # Track wine object

        elif self.selected_item == "veneno":
            # Place the Veneno (poison) object on the canvas and update the matrix with its value
            veneno_obj = Veneno()
            self.laberinto.matriz[fila][columna] = 3  # Represent poison with value 3 in the matrix
            x = columna * self.cell_size + self.cell_size // 2
            y = fila * self.cell_size + self.cell_size // 2
            image_id = self.laberinto_canvas.create_image(x, y, image=self.icons["veneno"])
            self.placed_images[(fila, columna)] = image_id
            # Optionally track the Veneno object in a list if needed for further use

        elif self.selected_item == "roca":
            # Place the rock on the canvas and mark in the maze matrix with value 1
            self.laberinto.matriz[fila][columna] = 1  # 1 represents a rock in the matrix
            roca_image_resized = ImageTk.PhotoImage(Image.open("icons/roca.png").resize((self.cell_size, self.cell_size)))
            x = columna * self.cell_size + self.cell_size // 2
            y = fila * self.cell_size + self.cell_size // 2
            image_id = self.laberinto_canvas.create_image(x, y, image=roca_image_resized)
            self.placed_images[(fila, columna)] = image_id
            self.placed_images[f"roca_{fila}_{columna}"] = roca_image_resized  # Save resized image reference

        elif self.selected_item == "meta":
            # Place the goal ("meta") and update position in the maze matrix
            self.laberinto.establecer_meta(fila, columna)
            x_centro = columna * self.cell_size + self.cell_size // 2
            y_centro = fila * self.cell_size + self.cell_size // 2
            image_id = self.laberinto_canvas.create_image(x_centro, y_centro, image=self.icons["meta"])
            self.placed_images[(fila, columna)] = image_id

        # Check if the goal is accessible after placing it
        if not self.laberinto.verificar_meta_accesible():
                messagebox.showwarning("Advertencia", "La meta no es accesible con este ítem. No puede estar rodeada de rocas.")
                # Remove the meta from the matrix and canvas if it’s inaccessible
                self.laberinto.matriz[fila][columna] = 0
                self.laberinto_canvas.delete(self.placed_images.get((fila, columna)))
                if (fila, columna) in self.placed_images:
                    del self.placed_images[(fila, columna)]
                self.laberinto.meta_posición = None  # Clear the meta position

        # Check if the goal is accessible after placing the new item
        if not self.laberinto.verificar_meta_accesible():
                # If inaccessible, revert the placement
                messagebox.showwarning("Advertencia", "La meta no es accesible con este ítem. No puede estar rodeada de rocas.")
                # Remove the newly placed item from the matrix and canvas
                self.laberinto.matriz[fila][columna] = 0
                self.laberinto_canvas.delete(self.placed_images.get((fila, columna)))
                if (fila, columna) in self.placed_images:
                    del self.placed_images[(fila, columna)]

        self.laberinto.mostrar_laberinto()


    def limpiar_canvas(self):
        """Limpia el canvas y restablece la matriz y referencias de imágenes."""
        # Elimina todos los elementos en el canvas
        self.laberinto_canvas.delete("all")
        
        # Limpia la matriz del laberinto y las referencias de imágenes
        self.laberinto = Laberinto(self.tamaño)  # Restablece la matriz
        self.placed_images.clear()  # Elimina todas las referencias de imágenes
        self.hormiga = None  # Elimina la referencia a la hormiga
        self.posición_hormiga = None  # Restablece la posición de la hormiga
        
        # Vuelve a crear el laberinto en el canvas
        self.crear_laberinto()

        self.laberinto.mostrar_laberinto()




    
    def iniciar_simulacion(self):
        # Verificar si la posición de la hormiga ha sido establecida
        if not self.posición_hormiga:
            messagebox.showwarning("Advertencia", "Debe colocar la posición inicial de la hormiga antes de iniciar.")
            return
        
        # Verificar si la posición de la meta ha sido establecida
        if not self.laberinto.meta_posición:
            messagebox.showwarning("Advertencia", "Debe colocar la meta en el laberinto antes de iniciar la simulación.")
            return

        # Si la meta y la hormiga están correctamente colocadas, se inicia la simulación
        self.running_simulation = True
        mejor_secuencia = self.algoritmo_genetico.evolucionar(self.laberinto, self.hormiga)
        
        # Extrae solo la secuencia de movimientos
        secuencia_movimientos = mejor_secuencia[0]

        # Llama a simular_movimiento con la secuencia de movimientos
        self.simular_movimiento(secuencia_movimientos)

    def ejecutar_simulacion(self):
        """Execute the simulation using an evolved sequence."""
        mejor_secuencia = self.algoritmo_genetico.evolucionar(self.laberinto, self.hormiga)
        self.simular_movimiento(mejor_secuencia)


    def simular_movimiento(self, secuencia, index=0):
        """Animate the movements in the sequence one by one with a delay."""
        if index >= len(secuencia):
            self.finalizar_simulacion()
            return

        movimiento = secuencia[index]
        self.hormiga.mover(movimiento, self.laberinto)

        if self.hormiga.posición == self.laberinto.meta_posición:
            self.finalizar_simulacion()
            return

        self.root.after(500, self.simular_movimiento, secuencia, index + 1)

    def iniciar_movimiento_aleatorio(self):
        """Start the ant's random movement until it reaches the goal."""
        if not self.posición_hormiga:
            messagebox.showwarning("Advertencia", "Debe colocar la posición inicial de la hormiga antes de iniciar.")
            return
        if not self.laberinto.meta_posición:
            messagebox.showwarning("Advertencia", "Debe colocar la meta en el laberinto antes de iniciar la simulación.")
            return

        # Begin the random movement process
        self.mover_aleatorio()

    def mover_aleatorio(self):
        """Randomly moves the ant in one direction until it reaches the goal."""
        # Check if the ant has reached the goal before moving
        if self.hormiga.posición == self.laberinto.meta_posición:
            self.finalizar_simulacion()

        # Generate a random direction and move the ant
        random_direction = random.choice(["arriba", "abajo", "izquierda", "derecha"])
        self.hormiga.mover(random_direction, self.laberinto)

        # Continue moving after a delay
        self.root.after(50, self.mover_aleatorio)  # Decreased delay to improve smoothness


    def detener_simulacion(self):
        """Stops the simulation when the ant consumes venom."""
        self.running_simulation = False  # Stops any ongoing movement
        messagebox.showinfo("Simulación", "La hormiga ha muerto por consumir veneno. La simulación se ha detenido.")
    
    def crear_nueva_hormiga(self, posición):
        """Creates a new Hormiga at the given position."""
        fila, columna = posición
        print(f"Creando nueva hormiga en la posición {posición}")
        
        # Create a new Hormiga instance at the specified position
        self.hormiga = Hormiga(posición, self.laberinto_canvas, self)

        # Update the matrix to mark the new Hormiga's position
        self.laberinto.matriz[fila][columna] = 6  # Use '6' to represent the Hormiga in the matrix
        
        # Place the new Hormiga on the canvas
        x = columna * self.cell_size + self.cell_size // 2
        y = fila * self.cell_size + self.cell_size // 2
        self.laberinto_canvas.coords(self.hormiga.hormiga_imagen, x, y)  # Position the image correctly

    def finalizar_simulacion(self):
        """Handle the end of a simulation iteration when the goal is reached."""
        if messagebox.askokcancel("Simulación", "¡La hormiga ha alcanzado la meta! ¿Desea continuar con una nueva simulación?"):
            self.hormiga = Hormiga(self.hormiga.posición, self.laberinto_canvas, self)  # Create new Hormiga
            self.ejecutar_simulacion()  # Run again with new evolved sequence
        else:
            self.running_simulation = False

if __name__ == "__main__":
    root = tk.Tk()
    app = LaberintoApp(root)
    root.mainloop()
