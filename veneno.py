from PIL import Image, ImageTk

class Veneno:
    def __init__(self):
        """
        Initializes the Veneno (poison) object and loads its image.
        """
        self.imagen = ImageTk.PhotoImage(Image.open("icons/veneno.png"))  # Load the poison image

    def consumir(self, hormiga):
        """
        Defines the effect of poison on the ant.
        
        :param hormiga: The ant instance that consumes the poison.
        """
        hormiga.salud = 0  # Reduces health to zero
        print("Hormiga ha consumido veneno. Salud reducida a cero.")
