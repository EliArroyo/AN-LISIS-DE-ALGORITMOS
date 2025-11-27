# Elizabeth Arroyo Moreno
# Problema del viajero (Traveling Salesman Problem)

#Importar librerías para trabajar con permutaciones (todas las rutas posibles).
from itertools import permutations 

#Los costos de las aristas entre las ciudades se representan en una matriz donde el valor en la fila i y columna j indica la distancia entre la ciudad i y la ciudad j.
distancia =[
    [28, 10, 15, 20, 30, 9],
    [10, 11, 35, 25, 30, 8],
    [15, 35, 4 , 30, 20, 25],
    [28, 39, 36, 22, 15, 17],
    [30, 25, 17, 15, 1, 3],
    [34, 20, 10, 17, 12, 19]
]
# Las ciudades se representan usando una lista,cada ciudad tiene un nombre que son las letras de la A a la F.
# Cada ciudad corresponde a un índice en la matriz de distancias.
ciudades = ["A", "B", "C", "D", "E", "F"]

# Se crea una función para calcular la distancia total de una ruta dada.
#La función toma una ruta (una permutación de ciudades) y la matriz de distancias como parámetros.
def calcular_distancia(ruta, distancia): 
    distancia_total = 0  
    for i in range(len(ruta) - 1): # Se utiliza un for para recorrer la ruta de ciudad en ciudad 
        ciudad_actual = ruta[i]  # Ciudad actual 
        ciudad_siguiente = ruta[i + 1] # Ciudad siguiente
        distancia_total += distancia[ciudad_actual][ciudad_siguiente] #  Incrementa la distancia total a medida que avanza en la ruta. Usa los costos de la matriz de distancias.
    distancia_total += distancia[ruta[-1]][ruta[0]]  # Se añade la distancia de regreso a la ciudad de origen.
    return distancia_total


# Funcion principal para resolver el problema del viajero.
def problema_viajero(distancia): #Se toma la matriz de distancias como parámetro.
    n = len(distancia) # Número de ciudades en la matriz de distancias.
    ciudades_idx = list(range(n)) # Enumera las ciudades por sus índices.
    distancia_min = float('inf') # Se inicializa la distancia mínima con infinito para asegurar que cualquier distancia calculada será menor.
    mejor_ruta = None # La mejor ruta se inicializa como None.
    

    # Se generan todas las permutaciones posibles de las ciudades y se calcula la distancia para cada una.
    for perm in permutations(ciudades_idx):
        distancia_actual = calcular_distancia(perm, distancia) # La distancia_actual se calcula para la permutación actual tomando la matriz de distancias.
        if distancia_actual < distancia_min: # Si la distancia actual es menor que la distancia mínima registrada la actualiza.
            distancia_min = distancia_actual 
            mejor_ruta = perm   # La mejor ruta se actualiza con la permutación actual.
   
    # Retorna la mejor ruta y la distancia mínima encontrada.
    return mejor_ruta, distancia_min 

# Función principal del programa
if __name__ == "__main__":
    print ("Problema del viajero (Traveling Salesman Problem)")

# Muestra todas las rutas posibles con sus distancias.
for perm in permutations(range(len(ciudades))): 
    nombre_ruta = ' -> '.join([ciudades[i] for i in perm]) # Convierte los índices en los nombres de ciudades para unirlos con una flecha.
    distancia_ruta = calcular_distancia(perm, distancia) # Calcula la distancia total de la ruta actual.
    print(f"Ruta: {nombre_ruta} | Distancia recorrida: {distancia_ruta}") # Imprime la ruta y su distancia total
mejor_ruta, distancia_min = problema_viajero(distancia) # Llama a la función para encontrar la mejor ruta y la distancia mínima
ruta_optima = ' -> '.join([ciudades[i] for i in mejor_ruta]) # Se convierten los índices a los nombres de las ciudades.
print(f"\nMejor ruta encontrada: {ruta_optima}, Distancia mínima: {distancia_min}")  # Imprime la mejor ruta y su distancia mínima.

