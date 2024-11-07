from PIL import Image, ImageTk

class Azucar:
    def __init__(self, puntos=10):
        """
        Inicializa el objeto Azúcar con la cantidad de puntos que otorga al ser consumido y carga su imagen.
        
        :param puntos: Cantidad de puntos que la hormiga recibe al consumir el azúcar.
        """
        self.puntos = puntos
        self.imagen = ImageTk.PhotoImage(Image.open("icons/azucar.png"))  # Ajusta el tamaño según sea necesario

    def consumir(self, hormiga):
        """
        Método que otorga puntos a la hormiga al consumir el azúcar y lo elimina de la casilla.
        
        :param hormiga: La instancia de la hormiga que consume el azúcar.
        """
        hormiga.puntos += self.puntos
        # Aquí podemos agregar la lógica para "eliminar" el azúcar de la casilla, si fuera necesario.
        
    def __str__(self):
        """
        Representación en cadena del objeto Azúcar, útil para depuración.
        """
        return f"Azúcar: +{self.puntos} puntos"
