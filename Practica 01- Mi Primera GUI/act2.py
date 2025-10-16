import tkinter as tk

def saludar():
    nombre = entrada.get().strip()
    if not nombre:
        nombre = "mundo"
    lbl.config(text=f"Buen dia, {nombre} 👋")

root = tk.Tk()
root.title("HOLA HOLA HOLA")
root.geometry("310x215")


lbl = tk.Label(root, text=" Como te llamas? presiona el botón")
lbl.pack(pady=8)

entrada = tk.Entry(root)
entrada.pack(pady=2)

btn = tk.Button(root, text="Saludar", command= Saludar)
btn.pack(pady=8)

btn = tk.Button(root, text="Saludar2", command= Saludar)
btn.pack(pady=8)


root.mainloop()

