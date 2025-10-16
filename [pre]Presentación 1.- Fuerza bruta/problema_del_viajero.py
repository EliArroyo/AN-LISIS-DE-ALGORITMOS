#Elizabeth Arroyo Moreno
#221453749

import itertools

class TSP:
    def __init__(self):
        self.nodos = ['A', 'B', 'C', 'D']
        self.n = len(self.nodos)
        
        self.matriz = [
            #   A    B    C    D
            [  0,   2,   5,   7],  # A
            [  2,   0,   8,   3],  # B  
            [  5,   8,   0,   1],  # C
            [  7,   3,   1,   0]   # D
        ]
        
    def mostrar_grafo(self):
        print("="*60)
        print("Grafo del Problema del Viajero.")
        print("="*60)
        print("\nMatriz de distancias del grafo:")
        print("-"*60)
        print("    ", end="")
        for nodo in self.nodos:
            print(f"{nodo:4}", end="")
        print()
        
        for i, nodo in enumerate(self.nodos):
            print(f"{nodo} ", end="")
            for j in range(self.n):
                print(f"{self.matriz[i][j]:4}", end="")
            print()
        
        print("\nPeso de cada arista:")
        print("A-B: 2")
        print("B-D: 3") 
        print("D-C: 1")
        print("C-A: 5")
        print("A-D: 7")
        print("B-C: 8")
    
    def calcular_costo_ruta(self, ruta):
        costo_total = 0
        for i in range(len(ruta)):
            desde = ruta[i]
            hacia = ruta[(i + 1) % len(ruta)]  
            costo = self.matriz[desde][hacia]
            costo_total += costo
        return costo_total
    
    def fuerza_bruta(self, nodo_inicio=0):
        otros_nodos = [i for i in range(self.n) if i != nodo_inicio]
        
        mejor_ruta = None
        mejor_costo = float('inf')
        
        print("Caminos posibles desde A:")
        
        for perm in itertools.permutations(otros_nodos):
            ruta_completa = [nodo_inicio] + list(perm) + [nodo_inicio]
            ruta_indices = [nodo_inicio] + list(perm)
            
            costo = self.calcular_costo_ruta(ruta_indices)
            ruta_nombres = [self.nodos[i] for i in ruta_completa]
            
            print(f"Ruta: {' -> '.join(ruta_nombres)}, Costo: {costo}")
            
            if costo < mejor_costo:
                mejor_costo = costo
                mejor_ruta = ruta_nombres
        
        return mejor_ruta, mejor_costo

def main():
    tsp = TSP()
    tsp.mostrar_grafo()
    
    print("\n" + "="*60)
    print("FUERZA BRUTA")
    print("="*60)
    
    mejor_ruta, mejor_costo = tsp.fuerza_bruta(nodo_inicio=0)
    print("-"*60)
    print(f"\nEl mejor recorrido encontrado es:")

    print(f"{' -> '.join(mejor_ruta)}")
    print(f"Costo total: {mejor_costo}")
    print("\n")

if __name__ == "__main__":
    main()