import random
import math
import time
import matplotlib.pyplot as plt
from hormiga import Hormiga

# Actions as alleles
ACTIONS = ["arriba", "abajo", "izquierda", "derecha"]

class AlgoritmoGenetico:
    def __init__(self, tamaño_poblacion=20, tasa_mutacion=0.1, generaciones=50):
        """
        Initialize the genetic algorithm with base parameters.

        :param tamaño_poblacion: Number of movement sequences in each generation.
        :param tasa_mutacion: Mutation probability for each allele.
        :param generaciones: Maximum number of generations to evolve.
        """
        self.tamaño_poblacion = tamaño_poblacion
        self.tasa_mutacion = tasa_mutacion
        self.generaciones = generaciones
        self.poblacion = self.inicializar_poblacion()

        self.tamaño_poblacion = tamaño_poblacion
        self.tasa_mutacion = tasa_mutacion
        self.generaciones = generaciones
        self.poblacion = self.inicializar_poblacion()
        self.mejor_puntajes_por_generacion = []
        self.tiempos_por_generacion = []
        self.mejor_puntaje_global = -float('inf')
        

        # For statistics tracking
        self.mejor_puntajes_por_generacion = []
        self.tiempos_por_generacion = []
        self.mejor_puntaje_global = -float('inf')  # Track the global best score
        self.no_mejora_contador = 0  # Count of consecutive generations without improvement

    def inicializar_poblacion(self):
        return [[random.choice(ACTIONS) for _ in range(10)] for _ in range(self.tamaño_poblacion)]
    
    def evaluar_fitness(self, secuencia, laberinto, hormiga):
        hormiga.reiniciar()
        fitness = 0
        meta_fila, meta_columna = laberinto.meta_posición

        for movimiento in secuencia:
            if isinstance(movimiento, str):
                hormiga.mover(movimiento, laberinto)
                fila, columna = hormiga.posición

                if 0 <= fila < laberinto.tamaño[0] and 0 <= columna < laberinto.tamaño[1]:
                    distancia_meta = math.sqrt((meta_fila - fila) ** 2 + (meta_columna - columna) ** 2)
                    fitness -= distancia_meta
                    if (fila, columna) == (meta_fila, meta_columna):
                        fitness += 1000
                        break
                else:
                    fitness -= 50
            else:
                print(f"Error: 'movimiento' is not a string, got {movimiento}")
        return fitness

    def evolucionar(self, laberinto, hormiga):
        best_fitness = float('-inf')
        gen_no_improvement = 0
        
        for gen in range(self.generaciones):
            start_time = time.time()

            self.poblacion = [(seq, self.evaluar_fitness(seq, laberinto, hormiga)) for seq in self.poblacion]
            self.poblacion.sort(key=lambda x: x[1], reverse=True)
            
            current_best_fitness = self.poblacion[0][1]
            if current_best_fitness > best_fitness:
                best_fitness = current_best_fitness
                gen_no_improvement = 0
            else:
                gen_no_improvement += 1

            self.mejor_puntajes_por_generacion.append(current_best_fitness)
            self.tiempos_por_generacion.append(time.time() - start_time)

            if gen > 2 and gen_no_improvement >= 3:
                print(f"Stopping early at Generation {gen} due to lack of improvement.")
                break

            seleccionados = self.seleccionar()
            nueva_poblacion = self.generar_nueva_poblacion(seleccionados)

            self.poblacion = [(seq, None) for seq in nueva_poblacion[:self.tamaño_poblacion]]

        return self.poblacion[0][0]
    
    def seleccionar(self):
        self.poblacion.sort(key=lambda x: x[1], reverse=True)
        return [seq for seq, _ in self.poblacion[:self.tamaño_poblacion // 2]]

    def cruzar(self, padre1, padre2):
        punto_corte = random.randint(1, len(padre1) - 2)
        hijo1 = padre1[:punto_corte] + padre2[punto_corte:]
        hijo2 = padre2[:punto_corte] + padre1[punto_corte:]
        return hijo1, hijo2
        
    def flatten_sequence(self, sequence):
        """Ensures the sequence is flat and contains only strings."""
        return [str(move[0] if isinstance(move, list) else move) for move in sequence]

    def mutar(self, secuencia):
        """Mutate each action in the sequence based on mutation probability."""
        return [random.choice(ACTIONS) if random.random() < self.tasa_mutacion else accion for accion in secuencia]

    def evolucionar(self, laberinto, hormiga):
        best_fitness = float('-inf')  # Track the best fitness score
        gen_no_improvement = 0  # Track generations without improvement

        for gen in range(self.generaciones):
            # Evaluate fitness of each sequence in the population and store as (sequence, fitness)
            self.poblacion = [(secuencia, self.evaluar_fitness(secuencia, laberinto, hormiga)) for secuencia in self.poblacion]
            
            # Sort population by fitness in descending order
            self.poblacion.sort(key=lambda x: x[1], reverse=True)
            
            # Get the current best fitness in this generation
            current_best_fitness = self.poblacion[0][1]
            if current_best_fitness > best_fitness:
                best_fitness = current_best_fitness
                gen_no_improvement = 0  # Reset counter if improvement occurs
            else:
                gen_no_improvement += 1  # Increment if no improvement
            
            # Log the structure for debugging purposes
            for i, item in enumerate(self.poblacion):
                if not isinstance(item, tuple) or len(item) != 2:
                    print(f"Warning: Unexpected item structure in population at index {i}: {item}")

            # Stop early if no improvement for the last 3 generations
            if gen > 2 and gen_no_improvement >= 3:
                print(f"Stopping early due to no improvement in last 3 generations (Generation {gen})")
                break

            # Selection
            seleccionados = self.seleccionar()

            # Create new generation via crossover and mutation
            nueva_poblacion = []
            while len(nueva_poblacion) < self.tamaño_poblacion:
                padre1, padre2 = random.sample(seleccionados, 2)
                hijo1, hijo2 = self.cruzar(padre1, padre2)
                nueva_poblacion.extend([self.mutar(hijo1), self.mutar(hijo2)])

            # Update population with the newly created generation
            self.poblacion = nueva_poblacion[:self.tamaño_poblacion]

        # Return the best sequence found
        mejor_secuencia = self.poblacion[0][0]  # This is the best sequence based on sorting
        return mejor_secuencia
    
    def validar_y_mutar(self, secuencia):
        """Ensure that each element in secuencia is a valid action and mutate if needed."""
        return [
            random.choice(ACTIONS) if random.random() < self.tasa_mutacion else accion
            for accion in secuencia if isinstance(accion, str)
        ]
    

    def generar_nueva_poblacion(self, seleccionados):
        nueva_poblacion = []
        while len(nueva_poblacion) < self.tamaño_poblacion:
            padre1, padre2 = random.sample(seleccionados, 2)
            hijo1, hijo2 = self.cruzar(padre1, padre2)
            nueva_poblacion.extend([self.validar_y_mutar(hijo1), self.validar_y_mutar(hijo2)])
        return nueva_poblacion

    def graficar_estadisticas(self):
        plt.figure(figsize=(12, 6))

        plt.subplot(1, 2, 1)
        plt.plot(self.mejor_puntajes_por_generacion, label='Mejor Puntaje por Generación')
        plt.xlabel('Generación')
        plt.ylabel('Mejor Puntaje')
        plt.title('Evolución del Mejor Puntaje')
        plt.legend()

        plt.subplot(1, 2, 2)
        plt.plot(self.tiempos_por_generacion, label='Tiempo por Generación', color='orange')
        plt.xlabel('Generación')
        plt.ylabel('Tiempo (segundos)')
        plt.title('Tiempo Promedio por Generación')
        plt.legend()

        plt.tight_layout()
        plt.show()