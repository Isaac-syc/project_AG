import random
import math
import matplotlib.pyplot as plt
from itertools import combinations
import tkinter as tk

# Variables globales para configuración
DIMENSIONES = (1000, 1000)
NUM_DESTINOS = 15
POBLACION_INICIAL = 50
NUM_GENERACIONES = 100
TASA_MUTACION = 0.1

# Función para solicitar parámetros
def solicitar_parametros_iniciales():
    root = tk.Tk()
    root.title("Parámetros para el Algoritmo Genético")

    # variables para almacenar la entrada del usuario
    dim_x = tk.IntVar(value=DIMENSIONES[0])
    dim_y = tk.IntVar(value=DIMENSIONES[1])
    num_destinos = tk.IntVar(value=NUM_DESTINOS)
    poblacion_inicial = tk.IntVar(value=POBLACION_INICIAL)
    num_generaciones = tk.IntVar(value=NUM_GENERACIONES)

    # Crear campos de entrada
    tk.Label(root, text="Ancho de la cuadrícula:").grid(row=0, column=0)
    tk.Entry(root, textvariable=dim_x).grid(row=0, column=1)

    tk.Label(root, text="Alto de la cuadrícula:").grid(row=1, column=0)
    tk.Entry(root, textvariable=dim_y).grid(row=1, column=1)

    tk.Label(root, text="Número de puntos destino:").grid(row=2, column=0)
    tk.Entry(root, textvariable=num_destinos).grid(row=2, column=1)

    tk.Label(root, text="Tamaño de la población inicial:").grid(row=3, column=0)
    tk.Entry(root, textvariable=poblacion_inicial).grid(row=3, column=1)

    tk.Label(root, text="Número de generaciones:").grid(row=4, column=0)
    tk.Entry(root, textvariable=num_generaciones).grid(row=4, column=1)

    # evento del botón
    def on_button_click():
        global DIMENSIONES, NUM_DESTINOS, POBLACION_INICIAL, NUM_GENERACIONES
        DIMENSIONES = (dim_x.get(), dim_y.get())
        NUM_DESTINOS = num_destinos.get()
        POBLACION_INICIAL = poblacion_inicial.get()
        NUM_GENERACIONES = num_generaciones.get()
        root.destroy()

    # Boton para iniciar el algoritmo
    button = tk.Button(root, text="Iniciar Algoritmo Genético", command=on_button_click)
    button.grid(row=5, column=0, columnspan=2)

    root.mainloop()

solicitar_parametros_iniciales()
CENTRO = (DIMENSIONES[0] // 2, DIMENSIONES[1] // 2)

# Generar puntos destino de manera aleatoria
def generar_puntos_destino(num_destinos, dimensiones):
    return [(random.randint(0, dimensiones[0]), random.randint(0, dimensiones[1])) for _ in range(num_destinos)]

# calcular la distancia euclidiana
def distancia(punto1, punto2):
    return math.hypot(punto1[0] - punto2[0], punto1[1] - punto2[1])

# Clase para representar un conjunto disjunto
class DisjointSet:
    def __init__(self, n):
        self.parent = list(range(n))

    def find(self, item):
        if self.parent[item] == item:
            return item
        else:
            self.parent[item] = self.find(self.parent[item])
            return self.parent[item]

    def union(self, set1, set2):
        root1 = self.find(set1)
        root2 = self.find(set2)
        self.parent[root1] = root2

# Función para construir un MST
def construir_mst(puntos_destino):
    puntos = [CENTRO] + puntos_destino
    aristas = [(distancia(punto1, punto2), punto1, punto2) for punto1, punto2 in combinations(puntos, 2)]
    aristas.sort()
    conjuntos = DisjointSet(len(puntos))
    mst = []
    for dist, punto1, punto2 in aristas:
        set1 = puntos.index(punto1)
        set2 = puntos.index(punto2)
        if conjuntos.find(set1) != conjuntos.find(set2):
            conjuntos.union(set1, set2)
            mst.append((punto1, punto2))
    return mst

# Función de aptitud
def funcion_aptitud(puntos_destino):
    mst = construir_mst(puntos_destino)
    return -sum(distancia(punto1, punto2) for punto1, punto2 in mst)

# Crear un individuo
def crear_individuo():
    return generar_puntos_destino(NUM_DESTINOS, DIMENSIONES)

# Crear población inicial
def crear_poblacion_inicial():
    return [crear_individuo() for _ in range(POBLACION_INICIAL)]

# Mutación
def mutacion(individuo):
    if random.random() < TASA_MUTACION:
        idx = random.randint(0, len(individuo) - 1)
        individuo[idx] = (random.randint(0, DIMENSIONES[0]), random.randint(0, DIMENSIONES[1]))
    return individuo

# Cruza
def cruza(padre1, padre2):
    mitad = len(padre1) // 2
    hijo1 = padre1[:mitad] + padre2[mitad:]
    hijo2 = padre2[:mitad] + padre1[mitad:]
    return [hijo1, hijo2]

# Selección y reproducción
def seleccion_y_reproduccion(poblacion):
    poblacion_ordenada = sorted(poblacion, key=funcion_aptitud, reverse=True)
    seleccionados = poblacion_ordenada[:POBLACION_INICIAL // 2]
    hijos = []
    while len(hijos) < POBLACION_INICIAL // 2:
        padre1, padre2 = random.sample(seleccionados, 2)
        hijos.extend(cruza(padre1, padre2))
    nueva_poblacion = seleccionados + hijos
    return nueva_poblacion

def algoritmo_genetico():
    poblacion = crear_poblacion_inicial()
    historial_aptitud = []

    for generacion in range(NUM_GENERACIONES):
        poblacion_mutada = [mutacion(individuo) for individuo in poblacion]
        poblacion = seleccion_y_reproduccion(poblacion_mutada)
        mejor_aptitud = funcion_aptitud(poblacion[0])
        historial_aptitud.append(mejor_aptitud)
        print(f"Generación {generacion}: Aptitud del mejor Individuo = {mejor_aptitud}")

    # Mostrar la aptitud del mejor individuo
    root = tk.Tk()
    root.title("Resultado del Algoritmo Genético")
    mensaje = f"Aptitud del mejor individuo en la última generación: {mejor_aptitud}"
    tk.Label(root, text=mensaje).pack(padx=20, pady=20)
    tk.Button(root, text="Cerrar", command=root.destroy).pack(pady=20)
    root.mainloop()

    return poblacion[0], historial_aptitud

# Visualización
def visualizar_red(puntos_destino):
    mst = construir_mst(puntos_destino)
    plt.figure(figsize=(10, 10))
    plt.plot(CENTRO[0], CENTRO[1], 'ro')
    for punto1, punto2 in mst:
        plt.plot([punto1[0], punto2[0]], [punto1[1], punto2[1]], 'g-')
    x, y = zip(*puntos_destino)
    plt.scatter(x, y, c='b')
    plt.title("Red de tuberías")
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.show()

# Ejecución del algoritmo genético
centro = (DIMENSIONES[0] // 2, DIMENSIONES[1] // 2)
mejor_solucion, historial_aptitud = algoritmo_genetico()
visualizar_red(mejor_solucion)

# Grafica de la evolución de la aptitud
plt.figure()
plt.plot(historial_aptitud)
plt.title("Evolución de la Aptitud")
plt.xlabel("Generación")
plt.ylabel("Aptitud (Distancia total)")
plt.show()
