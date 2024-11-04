import tkinter as tk
from tkinter import simpledialog, messagebox
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
        self.celdas = []  # Guardará las referencias a los botones de la GUI
        self.posición_hormiga = None  # Posición inicial de la hormiga
        self.hormiga = None
        self.algoritmo_genetico = AlgoritmoGenetico()  # Instancia del algoritmo genético
        
        # Configuración de la interfaz
        self.configurar_interfaz()
        
    def configurar_interfaz(self):
        # Botón para elegir el tamaño del laberinto
        btn_tamaño = tk.Button(self.root, text="Elegir Tamaño del Laberinto", command=self.elegir_tamaño)
        btn_tamaño.grid(row=0, column=0, columnspan=3, pady=10)
        
        # Botón para iniciar la simulación
        btn_iniciar = tk.Button(self.root, text="Iniciar Simulación", command=self.iniciar_simulacion)
        btn_iniciar.grid(row=1, column=0, columnspan=3, pady=10)
        
        # Contenedor del laberinto
        self.laberinto_frame = tk.Frame(self.root)
        self.laberinto_frame.grid(row=2, column=0, columnspan=3, padx=10, pady=10)
        
        # Inicializa el laberinto con el tamaño predeterminado
        self.crear_laberinto()
        
    def elegir_tamaño(self):
        # Dialogo para obtener el tamaño del laberinto
        filas = simpledialog.askinteger("Filas", "Número de filas (min 3, max 10):", minvalue=3, maxvalue=10)
        columnas = simpledialog.askinteger("Columnas", "Número de columnas (min 3, max 10):", minvalue=3, maxvalue=10)
        
        if filas and columnas:
            self.tamaño = (filas, columnas)
            self.crear_laberinto()
        
    def crear_laberinto(self):
        # Limpia el contenedor y crea una nueva instancia de laberinto
        for widget in self.laberinto_frame.winfo_children():
            widget.destroy()
        
        self.laberinto = Laberinto(self.tamaño)
        self.celdas = []
        
        # Crea botones para cada celda del laberinto
        for i in range(self.tamaño[0]):
            fila = []
            for j in range(self.tamaño[1]):
                btn = tk.Button(self.laberinto_frame, width=4, height=2, command=lambda x=i, y=j: self.editar_celda(x, y))
                btn.grid(row=i, column=j)
                fila.append(btn)
            self.celdas.append(fila)
        
    def editar_celda(self, fila, columna):
        # Menú para elegir el ítem que se colocará en la celda
        item = simpledialog.askstring("Editar Celda", "Seleccione el ítem (azúcar, vino, veneno, roca, hormiga):")
        if item in ["azúcar", "vino", "veneno", "roca", "hormiga"]:
            if item == "hormiga":
                # Asegurarse de que solo haya una hormiga en el laberinto
                if self.posición_hormiga:
                    x, y = self.posición_hormiga
                    self.celdas[x][y].config(text="")
                self.posición_hormiga = (fila, columna)
                self.hormiga = Hormiga((fila, columna))  # Inicializa la hormiga en esta posición
            elif item == "azúcar":
                self.laberinto.matriz[fila][columna] = Azucar()
            elif item == "vino":
                self.laberinto.matriz[fila][columna] = Vino()
            elif item == "veneno":
                self.laberinto.matriz[fila][columna] = Veneno()
            # Actualiza el texto del botón y la matriz del laberinto
            self.celdas[fila][columna].config(text=item)
        else:
            messagebox.showwarning("Item no válido", "Por favor, elija un ítem válido.")
        
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
