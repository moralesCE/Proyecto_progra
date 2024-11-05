import tkinter as tk
from tkinter import messagebox, simpledialog
from PIL import Image, ImageTk
from laberinto import Laberinto
from hormiga import Hormiga
from azucar import Azucar
from vino import Vino
from veneno import Veneno
from algoritmo_genetico import AlgoritmoGenetico

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
        
        # Configuración de la interfaz
        self.configurar_interfaz()
        
    def configurar_interfaz(self):
        # Panel de herramientas para seleccionar íconos, en el lateral izquierdo
        self.toolbar = tk.Frame(self.root)
        self.toolbar.pack(side="left", padx=10, pady=10, fill="y")

        # Cargar imágenes de íconos
        self.icons = {
            "hormiga": tk.PhotoImage(file="icons/hormiga.png"),
            "azúcar": ImageTk.PhotoImage(Image.open("icons/azucar.png").resize((20, 25))),  # Más grande
            "vino": ImageTk.PhotoImage(Image.open("icons/vino.png").resize((20, 25))),      # Más grande
            "veneno": ImageTk.PhotoImage(Image.open("icons/veneno.png").resize((20, 25))),  # Más grande
            "roca": ImageTk.PhotoImage(Image.open("icons/roca.png").resize((26, 26)))
        }

        # Crear botones en la barra de herramientas para seleccionar elementos
        for item, icon in self.icons.items():
            btn = tk.Button(self.toolbar, image=icon, command=lambda i=item: self.seleccionar_item(i))
            btn.pack(pady=5)  # Separación vertical entre los botones

        # Botones principales encima del canvas
        control_frame = tk.Frame(self.root)
        control_frame.pack(pady=10)

        # Botón para elegir el tamaño del laberinto
        btn_tamaño = tk.Button(control_frame, text="Elegir Tamaño del Laberinto", command=self.elegir_tamaño)
        btn_tamaño.grid(row=0, column=0, padx=5)
        
        # Botón para iniciar la simulación
        btn_iniciar = tk.Button(control_frame, text="Iniciar Simulación", command=self.iniciar_simulacion)
        btn_iniciar.grid(row=0, column=1, padx=5)
        
        # Contenedor del laberinto en Canvas, al lado derecho del panel de herramientas
        self.laberinto_canvas = tk.Canvas(self.root)
        self.laberinto_canvas.pack(padx=10, pady=10)
        
        # Inicializa el laberinto con el tamaño predeterminado
        self.crear_laberinto()
        
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
        
        self.laberinto = Laberinto(self.tamaño)
        
        # Calcula el tamaño total del canvas basado en el tamaño de cada celda y el tamaño del laberinto
        filas, columnas = self.tamaño
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
                # Añade un binding al rectángulo para editar la celda
                self.laberinto_canvas.tag_bind(rect, "<Button-1>", lambda event, row=i, col=j: self.colocar_item(row, col))

    def colocar_item(self, fila, columna):
        """Coloca el ítem seleccionado en la posición del canvas."""
        if not self.selected_item:
            messagebox.showwarning("Advertencia", "Seleccione un ítem antes de colocarlo.")
            return

        color = "white"
        if self.selected_item == "hormiga":
            # Asegurarse de que solo haya una hormiga en el laberinto
            if self.posición_hormiga:
                x, y = self.posición_hormiga
                self.laberinto_canvas.itemconfig(self.laberinto_canvas.find_closest(x * self.cell_size, y * self.cell_size), fill="white")
            self.posición_hormiga = (fila, columna)
            self.hormiga = Hormiga((fila, columna))  # Inicializa la hormiga en esta posición
            color = "blue"
        elif self.selected_item == "azúcar":
            self.laberinto.matriz[fila][columna] = Azucar()
            color = "yellow"
        elif self.selected_item == "vino":
            self.laberinto.matriz[fila][columna] = Vino()
            color = "purple"
        elif self.selected_item == "veneno":
            self.laberinto.matriz[fila][columna] = Veneno()
            color = "red"
        elif self.selected_item == "roca":
            color = "gray"
        
        # Actualiza el color de la celda en el canvas
        x1 = columna * self.cell_size
        y1 = fila * self.cell_size
        x2 = x1 + self.cell_size
        y2 = y1 + self.cell_size
        self.laberinto_canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="black")
        
    def iniciar_simulacion(self):
        # Verifica que se haya seleccionado una posición inicial para la hormiga
        if not self.posición_hormiga:
            messagebox.showwarning("Advertencia", "Debe colocar la posición inicial de la hormiga antes de iniciar.")
            return
        
        # Ejecuta el algoritmo genético para encontrar la mejor secuencia
        mejor_secuencia = self.algoritmo_genetico.evolucionar(self.laberinto, self.hormiga)
        
        # Muestra la mejor secuencia de movimientos
        resultado = " -> ".join(mejor_secuencia)
        messagebox.showinfo("Resultado de la Simulación", f"La mejor secuencia encontrada es: {resultado}")
        
        # Actualiza el laberinto en consola para ver la distribución final (opcional para depuración)
        print("Estado final del laberinto:")
        for fila in self.laberinto.matriz:
            print(fila)

if __name__ == "__main__":
    root = tk.Tk()
    app = LaberintoApp(root)
    root.mainloop()
