import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np
import time
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# ---------------- Algoritmos de búsqueda ----------------
def busqueda_lineal(lista, x):
    for i, val in enumerate(lista):
        if val == x:
            return i
    return -1

def busqueda_binaria(lista, x):
    low, high = 0, len(lista) - 1
    while low <= high:
        mid = (low + high) // 2
        if lista[mid] == x:
            return mid
        elif lista[mid] < x:
            low = mid + 1
        else:
            high = mid - 1
    return -1

# ---------------- Interfaz gráfica que permite la búsqueda ----------------
class BusquedaApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Búsqueda Lineal vs Binaria")
        self.root.configure(bg="#E6E6FA")  # color de fondo
        self.lista = []

        # Tamaño de lista
        ttk.Label(root, text="Tamaño de la lista:", background="#E6E6FA").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.size_var = tk.StringVar(value="100") 
        self.size_menu = ttk.Combobox(root, textvariable=self.size_var, values=["100", "1000", "10000", "100000"], state="readonly")
        self.size_menu.grid(row=0, column=1, sticky="w", padx=5)

        # Botón Generar datos
        self.gen_button = tk.Button(root, text="Generar datos", command=self.generar_datos,
                                    bg="#9370DB", fg="white", activebackground="#7B68EE")
        self.gen_button.grid(row=0, column=2, padx=5, pady=5)

        # Entrada valor a buscar
        ttk.Label(root, text="Valor a buscar:", background="#E6E6FA").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.buscar_entry = tk.Entry(root, bg="white")
        self.buscar_entry.grid(row=1, column=1, sticky="w", padx=5)

        # Botones de búsqueda
        self.lineal_button = tk.Button(root, text="Búsqueda lineal", command=self.buscar_lineal,
                                       bg="#9370DB", fg="white", activebackground="#7B68EE")
        self.lineal_button.grid(row=2, column=0, pady=5, padx=5)
        self.binaria_button = tk.Button(root, text="Búsqueda binaria", command=self.buscar_binaria,
                                        bg="#9370DB", fg="white", activebackground="#7B68EE")
        self.binaria_button.grid(row=2, column=1, pady=5, padx=5)

        # Resultados
        self.result_label = tk.Label(root, text="Resultados aquí", fg="blue", bg="#E6E6FA")
        self.result_label.grid(row=3, column=0, columnspan=3, pady=5)

        # Gráfica
        self.fig, self.ax = plt.subplots(figsize=(5,3))
        self.canvas = FigureCanvasTkAgg(self.fig, master=root)
        self.canvas.get_tk_widget().grid(row=4, column=0, columnspan=3, pady=10)

        # Datos para comparación
        self.tiempos_promedio = {"Lineal": [], "Binaria": []}
        self.tamanos = [100, 1000, 10000, 100000]

        # Valor garantizado de prueba
        self.valor_existente = None

    # -------- Funciones de la aplición --------
    def generar_datos(self):
        try:
            size = int(self.size_var.get())
            self.lista = np.sort(np.random.randint(0, size*10, size)).tolist()
            self.valor_existente = np.random.choice(self.lista)
            messagebox.showinfo("Datos generados", f"Lista de tamaño {size} generada y ordenada.\nPrueba con un valor existente: {self.valor_existente}")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo generar la lista: {e}")

    def medir_tiempo(self, func, lista, valor, repeticiones=5):
        tiempos = []
        for _ in range(repeticiones):
            start = time.perf_counter()
            func(lista, valor)
            end = time.perf_counter()
            tiempos.append((end - start) * 1000)  # ms
        return np.mean(tiempos)

    def buscar_lineal(self):
        if not self.lista:
            messagebox.showwarning("Atención", "Primero genere la lista de datos.")
            return
        valor = self.validar_valor()
        if valor is None:
            return
        indice = busqueda_lineal(self.lista, valor)
        tiempo = self.medir_tiempo(busqueda_lineal, self.lista, valor)
        resultado = f"Búsqueda Lineal: {'No encontrado' if indice == -1 else f'Índice {indice}'} | Tiempo: {tiempo:.4f} ms"
        self.result_label.config(text=resultado)
        self.actualizar_grafica("Lineal", valor)

    def buscar_binaria(self):
        if not self.lista:
            messagebox.showwarning("Atención", "Primero genere la lista de datos.")
            return
        valor = self.validar_valor()
        if valor is None:
            return
        indice = busqueda_binaria(self.lista, valor)
        tiempo = self.medir_tiempo(busqueda_binaria, self.lista, valor)
        resultado = f"Búsqueda Binaria: {'No encontrado' if indice == -1 else f'Índice {indice}'} | Tiempo: {tiempo:.4f} ms"
        self.result_label.config(text=resultado)
        self.actualizar_grafica("Binaria", valor)

    def validar_valor(self):
        try:
            valor = int(self.buscar_entry.get())
            return valor
        except:
            if self.valor_existente is not None:
                self.buscar_entry.delete(0, tk.END)
                self.buscar_entry.insert(0, str(self.valor_existente))
                messagebox.showinfo("Sugerencia", f"Se usará un valor existente automáticamente: {self.valor_existente}")
                return self.valor_existente
            else:
                messagebox.showerror("Error", "Ingrese el valor numérico válido a buscar.")
                return None

    def actualizar_grafica(self, algoritmo, valor):
        self.tiempos_promedio[algoritmo] = []
        for size in self.tamanos:
            lista_temp = np.sort(np.random.randint(0, size*10, size)).tolist()
            tiempo = self.medir_tiempo(busqueda_lineal if algoritmo=="Lineal" else busqueda_binaria, lista_temp, valor)
            self.tiempos_promedio[algoritmo].append(tiempo)
        self.ax.clear()
        self.ax.plot(self.tamanos, self.tiempos_promedio["Lineal"], marker='o', label="Lineal")
        self.ax.plot(self.tamanos, self.tiempos_promedio["Binaria"], marker='o', label="Binaria")
        self.ax.set_xlabel("Tamaño de lista")
        self.ax.set_ylabel("Tiempo promedio (ms)")
        self.ax.set_title("Comparación de tiempos de búsqueda")
        self.ax.legend()
        self.ax.grid(True)
        self.canvas.draw()

# ---------------- Aplicación principal  ----------------
if __name__ == "__main__":
    root = tk.Tk()
    app = BusquedaApp(root)
    root.mainloop()
