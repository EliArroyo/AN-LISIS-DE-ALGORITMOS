# Elizabeth Arroyo Moreno

import math
import random
import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox


ctk.set_appearance_mode("light")  
ctk.set_default_color_theme("blue")  

FUENTE = ("Montserrat", 14)

# Funciones matemáticas  para calcular la distancia

def distancia(p1, p2):
    return math.sqrt((p2[0] - p1[0])**2 + (p2[1] - p1[1])**2)

def generar_datos(n=5, min_val=0, max_val=40): 
    return [(random.randint(min_val, max_val), random.randint(min_val, max_val)) for _ in range(n)]


def calcular_distancias(puntos):
    distancias = []
    i = 0
    while i < len(puntos):
        j = i + 1
        while j < len(puntos):
            d = distancia(puntos[i], puntos[j])
            distancias.append(((puntos[i], puntos[j]), d))
            j += 1
        i += 1
    return distancias

def generar_aleatorios():
    puntos = generar_datos()
    for idx, (entry_x, entry_y) in enumerate(entries):
        entry_x.delete(0, tk.END)
        entry_y.delete(0, tk.END)
        entry_x.insert(0, str(puntos[idx][0]))
        entry_y.insert(0, str(puntos[idx][1]))

def limpiar():
    for entry_x, entry_xy in entries:
        entry_x.delete(0, tk.END)
        entry_xy.delete(0, tk.END)
    texto_resultados.configure(state="normal")
    texto_resultados.delete("1.0", tk.END)
    texto_resultados.configure(state="disabled")

def calcular():
    try:
        puntos = []
        for entry_x, entry_y in entries:
            x_text = entry_x.get().strip()
            y_text = entry_y.get().strip()
            
            if not x_text or not y_text:
                raise ValueError("Todos los campos deben de estar completos")
            
            x = int(x_text)
            y = int(y_text)
            
            if not (0 <= x <= 40 and 0 <= y <= 40):
                raise ValueError("Valores fuera de rango (0-40)")
                
            puntos.append((x, y))

        distancias = calcular_distancias(puntos)
        distancias_ordenadas = sorted(distancias, key=lambda x: x[1])
        
        resultado = "*********** DISTANCIAS CALCULADAS ***********\n\n"
        for idx, ((p1, p2), d) in enumerate(distancias_ordenadas, 1):
            resultado += f"{idx} : {p1} - {p2} = {d:.5f}\n"

        mas_corta = distancias_ordenadas[0]
        resultado += f"\n" + "="*35 + "\n"
        resultado += f"DISTANCIA MÁS CORTA:\n"
        resultado += f"{mas_corta[0][0]} - {mas_corta[0][1]} = {mas_corta[1]:.5f}"

        texto_resultados.configure(state="normal")
        texto_resultados.delete("1.0", tk.END)
        texto_resultados.insert("1.0", resultado)
        texto_resultados.configure(state="disabled")

    except ValueError as e:
        messagebox.showerror("Error", f" {str(e)}")


# --- Ventana Principal ---
root = ctk.CTk()
root.title("Calculadora de Distancia entre Puntos")
root.geometry("650x650")


titulo = ctk.CTkLabel(root, text="Calculadora de Distancia", 
                     font=("Montserrat", 24, "bold"))
titulo.pack(pady=(20, 10))

subtitulo = ctk.CTkLabel(root, text="Encuentra el par más cercano", 
                        font=("Montserrat", 14), 
                        text_color="gray")
subtitulo.pack(pady=(0, 15))


frame_inputs = ctk.CTkFrame(root, corner_radius=20)
frame_inputs.pack(pady=10, padx=25, fill="x")

instrucciones = ctk.CTkLabel(frame_inputs, 
                            text="Ingresa las coordenadas (x, y) :", 
                            font=("Montserrat", 13))
instrucciones.pack(pady=(15, 10))

entries = []
for i in range(5):
    fila = ctk.CTkFrame(frame_inputs, corner_radius=10)
    fila.pack(pady=8, padx=15, fill="x")

    lbl = ctk.CTkLabel(fila, text=f"Punto {i+1}:", font=FUENTE, width=80)
    lbl.pack(side="left", padx=(10, 15))

    ctk.CTkLabel(fila, text="X:", font=FUENTE).pack(side="left", padx=(0, 5))
    ex = ctk.CTkEntry(fila, width=70, font=("Montserrat", 12), placeholder_text="0-40")
    ex.pack(side="left", padx=(0, 15))
    
    ctk.CTkLabel(fila, text="Y:", font=FUENTE).pack(side="left", padx=(0, 5))
    ey = ctk.CTkEntry(fila, width=70, font=("Montserrat", 12), placeholder_text="0-40")
    ey.pack(side="left", padx=(0, 10))

    entries.append((ex, ey))

#----------- Botones y Resultados de la GUI -----------
frame_botones = ctk.CTkFrame(root, corner_radius=15)
frame_botones.pack(pady=20)

btn_random = ctk.CTkButton(frame_botones, 
                          text=" Generar ", 
                          font=FUENTE, 
                          command=generar_aleatorios, 
                          fg_color="#ff8fab", 
                          hover_color="#ff5c8a", 
                          corner_radius=20,
                          width=150)
btn_random.pack(side="left", padx=8)

btn_clear = ctk.CTkButton(frame_botones, 
                         text="Limpiar", 
                         font=FUENTE, 
                         command=limpiar, 
                         fg_color="#ffb3ba", 
                         hover_color="#ff9aa2", 
                         corner_radius=20,
                         width=150)
btn_clear.pack(side="left", padx=8)

btn_calc = ctk.CTkButton(frame_botones, 
                        text="Calcular", 
                        font=("Montserrat", 14, "bold"), 
                        command=calcular, 
                        fg_color="#c77dff", 
                        hover_color="#9d4edd", 
                        corner_radius=20,
                        width=150,
                        height=30)
btn_calc.pack(side="left", padx=8)


label_resultados = ctk.CTkLabel(root, text="Resultados:", font=("Montserrat", 16, "bold"))
label_resultados.pack(pady=(15, 5))

texto_resultados = ctk.CTkTextbox(root, 
                                 width=580, 
                                 height=220, 
                                 font=("Consolas", 12),
                                 corner_radius=10)
texto_resultados.pack(pady=(0, 20), padx=25)
texto_resultados.configure(state="disabled")

root.mainloop()