import customtkinter as ctk
import tkinter as tk
import random
import time
from tkinter import messagebox


ANCHO = 1200 # Ancho del canvas
ALTO = 400 # Alto del canvas
N_BARRAS = 50 # Número inicial de barras
VAL_MIN, VAL_MAX = 5, 100
METODOS = ["Selection", "Bubble", "Merge", "Quick"]
RETARDO_MS = 50  # velocidad de animación x defecto

# Configuración del tema
ctk.set_appearance_mode("dark")   
ctk.set_default_color_theme("blue")  

# Colores de los botones al ser presionados
COLOR_BOTON = "#ae5ccc"   
COLOR_BOTON_HOVER = "#8a30b0"  

# -------------------- FUNCIONES DE ORDENAMIENTO --------------------

# ALGORITMO: SELECTION SORT
def selection_sort_steps(data, draw_callback):
    n = len(data)
    for i in range(n):
        min_idx = i
        for j in range(i + 1, n):
            draw_callback(activos=[i, j, min_idx])
            yield
            if data[j] < data[min_idx]:
                min_idx = j
        data[i], data[min_idx] = data[min_idx], data[i]
        draw_callback(activos=[i, min_idx])
        yield
    draw_callback(activos=[])

# ALGORITMO: BUBBLE SORT
def bubble_sort_steps(data, draw_callback):
    n = len(data)
    for i in range(n - 1):
        for j in range(0, n - i - 1):
            draw_callback(activos=[j, j + 1])
            yield
            if data[j] > data[j + 1]:
                data[j], data[j + 1] = data[j + 1], data[j]
                draw_callback(activos=[j, j + 1])
                yield
    draw_callback(activos=[])

# ALGORITMO: MERGE SORT
def merge_sort_steps(data, draw_callback, inicio=0, fin=None):
    if fin is None:
        fin = len(data)
    
    if fin - inicio > 1:
        medio = (inicio + fin) // 2
        yield from merge_sort_steps(data, draw_callback, inicio, medio)
        yield from merge_sort_steps(data, draw_callback, medio, fin)

        izquierda = data[inicio:medio]
        derecha = data[medio:fin]
        i = j = 0
        k = inicio
        
        while i < len(izquierda) and j < len(derecha):
            draw_callback(activos=[k])
            yield
            if izquierda[i] <= derecha[j]:
                data[k] = izquierda[i]
                i += 1
            else:
                data[k] = derecha[j]
                j += 1
            k += 1
            
        while i < len(izquierda):
            draw_callback(activos=[k])
            yield
            data[k] = izquierda[i]
            i += 1
            k += 1
            
        while j < len(derecha):
            draw_callback(activos=[k])
            yield
            data[k] = derecha[j]
            j += 1
            k += 1

# ALGORITMO: QUICK SORT
def quick_sort_steps(data, draw_callback, start=0, end=None):
    if end is None:
        end = len(data) - 1

    def particion(data, start, end):
        pivot = data[start]
        menor = start + 1
        mayor = end
        while True:
            while menor <= mayor and data[mayor] >= pivot:
                mayor -= 1
            while menor <= mayor and data[menor] <= pivot:
                menor += 1

            if menor <= mayor:
                draw_callback(activos=[menor, mayor])
                yield
                data[menor], data[mayor] = data[mayor], data[menor]
                draw_callback(activos=[menor, mayor])
                yield
            else:
                break
        draw_callback(activos=[start, mayor])
        yield
        data[start], data[mayor] = data[mayor], data[start]
        draw_callback(activos=[start, mayor])
        yield

        return mayor
    if start < end:
        gen = particion(data, start, end)
        for paso in gen:
            yield paso

        p = data[start:end+1].index(min(data[start:end+1])) + start  
        p = particion_index = yield from particion(data, start, end)

        yield from quick_sort_steps(data, draw_callback, start, particion_index - 1)
        yield from quick_sort_steps(data, draw_callback, particion_index + 1, end)

    if start == 0 and end == len(data) - 1:
        draw_callback(activos=[])

# -------------------- FUNCIONES DE DIBUJO --------------------
def dibujar_barras(canvas, datos, activos=None):
    canvas.delete("all")
    if not datos: 
        return
    
    n = len(datos)
    margen = 20
    ancho_disp = ANCHO - 2 * margen
    alto_disp = ALTO - 2 * margen
    w = ancho_disp / n
    esc = alto_disp / max(datos) if max(datos) > 0 else 1
    
    for i, v in enumerate(datos):
        x0 = margen + i * w
        x1 = x0 + w * 0.8
        h = v * esc
        y0 = ALTO - margen - h
        y1 = ALTO - margen
        color = "#06B4F9"  
        if activos and i in activos:
            color = "#FF00AA" 
        canvas.create_rectangle(x0, y0, x1, y1, fill=color, outline="")

    canvas.create_text(10, 10, anchor="nw", text=f"N: {len(datos)}", fill="white", font=("Montserrat", 16))

# -------------------- APLICACIÓN PRINCIPAL --------------------
datos = []
animando = False

root = ctk.CTk()
root.title("Visualizador - Métodos de Ordenamiento")
root.geometry("1300x650")

canvas = tk.Canvas(root, width=ANCHO, height=ALTO, bg="#0f0f1a", highlightthickness=0)
canvas.pack(padx=10, pady=10)

def generar():
    global datos, animando
    if animando:
        return
    random.seed(time.time())
    datos = [random.randint(VAL_MIN, VAL_MAX) for _ in range(N_BARRAS)]
    dibujar_barras(canvas, datos)

def mezclar():
    global datos, animando
    if animando or not datos:
        return
    random.shuffle(datos)
    dibujar_barras(canvas, datos)

def limpiar():
    global animando
    if animando:
        return
    dibujar_barras(canvas, datos)

def cambiar_n():
    global N_BARRAS, datos, animando
    if animando:
        return
    try:
        nuevo_n = int(entry_n.get())
        if 5 <= nuevo_n <= 100:
            N_BARRAS = nuevo_n
            generar()
        else:
            messagebox.showerror("Error", "Por favor ingrese un número entre 5 y 100.")
            entry_n.delete(0, tk.END)
            entry_n.insert(0, str(N_BARRAS))
    except ValueError:
        messagebox.showerror("Error", "Entrada inválida. Por favor ingrese un valor válido.")
        entry_n.delete(0, tk.END)
        entry_n.insert(0, str(N_BARRAS))

def obtener_velocidad():
    return int(velocidad_scale.get())

def ordenar():
    global animando
    if not datos or animando:
        return
    
    animando = True
    metodo = metodo_seleccion.get()
    
    # Crear copia de los datos para ordenar
    datos_copia = datos.copy()
    
    if metodo == "Selection":
        gen = selection_sort_steps(datos_copia, lambda activos=None: dibujar_barras(canvas, datos_copia, activos))
    elif metodo == "Bubble":
        gen = bubble_sort_steps(datos_copia, lambda activos=None: dibujar_barras(canvas, datos_copia, activos))
    elif metodo == "Merge":
        gen = merge_sort_steps(datos_copia, lambda activos=None: dibujar_barras(canvas, datos_copia, activos))
    elif metodo == "Quick":
        gen = quick_sort_steps(datos_copia, lambda activos=None: dibujar_barras(canvas, datos_copia, activos))
    else:
        animando = False
        return
    
    def paso():
        global animando
        try:
            next(gen)
            root.after(obtener_velocidad(), paso)
        except StopIteration:
            global datos
            datos = datos_copia
            dibujar_barras(canvas, datos)
            animando = False
    
    paso()

# -------------------- CONTROLES --------------------
# Frame principal de controles 
main_control_frame = ctk.CTkFrame(root)
main_control_frame.pack(pady=10, fill="x", padx=20)

# Primera fila de controles (N barras y método)
control_frame1 = ctk.CTkFrame(main_control_frame)
control_frame1.pack(pady=5, fill="x")

# Campo N  barras
ctk.CTkLabel(control_frame1, text="Número de elementos:", font=("Montserrat", 14)).pack(side="left", padx=5)
entry_n = ctk.CTkEntry(control_frame1, width=80, placeholder_text="N")
entry_n.insert(0, str(N_BARRAS))
entry_n.pack(side="left", padx=5)
ctk.CTkButton(control_frame1, text="Aplicar", command=cambiar_n, width=80,
              fg_color=COLOR_BOTON, hover_color=COLOR_BOTON_HOVER).pack(side="left", padx=5)

# Menú de métodos
ctk.CTkLabel(control_frame1, text="Algoritmo:", font=("Montserrat", 14)).pack(side="left", padx=(20, 5))
metodo_seleccion = tk.StringVar(value=METODOS[0])
menu = ctk.CTkOptionMenu(control_frame1, variable=metodo_seleccion, values=METODOS, width=120)
menu.pack(side="left", padx=5)

# Controles de Velocidad
control_frame2 = ctk.CTkFrame(main_control_frame)
control_frame2.pack(pady=5, fill="x")
ctk.CTkLabel(control_frame2, text="Velocidad (ms):", font=("Montserrat", 14)).pack(side="left", padx=5) # Etiqueta de velocidad
velocidad_scale = ctk.CTkSlider(control_frame2, from_=1, to=200, number_of_steps=99, width=300) # Slider de velocidad
velocidad_scale.set(RETARDO_MS)
velocidad_scale.pack(side="left", padx=10)

velocidad_label = ctk.CTkLabel(control_frame2, text=f"{int(velocidad_scale.get())} ms", font=("Montserrat", 14))
velocidad_label.pack(side="left", padx=5)

def actualizar_velocidad_label(value):
    velocidad_label.configure(text=f"{int(float(value))} ms")

velocidad_scale.configure(command=actualizar_velocidad_label)

# Botones principales (Generar, Mezclar y  Ordenar)
boton_frame = ctk.CTkFrame(main_control_frame)
boton_frame.pack(pady=10)

ctk.CTkButton(boton_frame, text="Generar", command=generar, width=120, corner_radius=20,
              fg_color=COLOR_BOTON, hover_color=COLOR_BOTON_HOVER, text_color="white",
              font=("Montserrat", 14, "bold")).pack(side="left", padx=10)

ctk.CTkButton(boton_frame, text="Mezclar", command=mezclar, width=120, corner_radius=20,
              fg_color=COLOR_BOTON, hover_color=COLOR_BOTON_HOVER, text_color="white",
              font=("Montserrat", 14, "bold")).pack(side="left", padx=10)

ctk.CTkButton(boton_frame, text="Ordenar", command=ordenar, width=120, corner_radius=20,
              fg_color="#ae5ccc", hover_color="#8a30b0", text_color="white",
              font=("Montserrat", 14, "bold")).pack(side="left", padx=10)


# ctk.CTkButton(boton_frame, text="Limpiar", command=limpiar, width=120, corner_radius=20,
#     fg_color="#ae5ccc", hover_color="#8a30b0", text_color="white",
#             font=("Montserrat", 14, "bold")).pack(side="left", padx=10)

generar()
root.mainloop()