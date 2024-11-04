class Veneno:
    def __init__(self):
        """
        Inicializa el objeto Veneno. No necesita atributos adicionales, ya que su efecto es mortal.
        """
        pass

    def consumir(self, hormiga):
        """
        Método que "mata" a la hormiga al consumir el veneno, reduciendo su salud a 0.
        
        :param hormiga: La instancia de la hormiga que consume el veneno.
        """
        hormiga.modificar_salud(-100)  # Reduce la salud de la hormiga a 0 para simular la muerte
        # Aquí se puede agregar la lógica para detener la simulación y eliminar el veneno de la casilla.
        
    def __str__(self):
        """
        Representación en cadena del objeto Veneno, útil para depuración.
        """
        return "Veneno: Mata a la hormiga"
