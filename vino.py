from PIL import Image, ImageTk

class Vino:
    def __init__(self, incremento_alcohol=10):
        """
        Inicializa el objeto Vino con la cantidad de incremento en el nivel de alcohol.
        
        :param incremento_alcohol: Cantidad de nivel de alcohol que se incrementa al consumir el vino.
        """
        self.incremento_alcohol = incremento_alcohol
        self.imagen = ImageTk.PhotoImage(Image.open("icons/vino.png"))

    def consumir(self, hormiga):
        """
        Método que aumenta el nivel de alcohol de la hormiga al consumir el vino y lo elimina de la casilla.
        
        :param hormiga: La instancia de la hormiga que consume el vino.
        """
        hormiga.modificar_nivel_alcohol(self.incremento_alcohol)
        # Aquí podemos agregar la lógica para "eliminar" el vino de la casilla, si fuera necesario.
        
    def __str__(self):
        """
        Representación en cadena del objeto Vino, útil para depuración.
        """
        return f"Vino: +{self.incremento_alcohol} nivel de alcohol"
