# Comparación de Algoritmos de Búsqueda (Lineal vs Binaria) - Python GUI

Esta aplicación permite **comparar la búsqueda lineal y la búsqueda binaria** en listas de distintos tamaños mediante una **interfaz gráfica en Python**. Muestra resultados numéricos y gráficos de los tiempos de ejecución.

---

## Requisitos

- **Python 3.x**
- Bibliotecas:
  ```bash
  pip install numpy matplotlib
Cómo ejecutar la aplicación
---


Entrar a el archivo:

cd ACT1_GUI.py


Instalar las dependencias (si no están instaladas):
 pip install numpy matplotlib


Ejecutar la aplicación:

python main.py

Cómo usar la aplicación
---
Selecciona el tamaño de la lista en el menú desplegable (100, 1,000, 10,000 o 100,000).

Haz clic en Generar datos para crear una lista ordenada de números aleatorios. Se te sugerirá un valor existente para probar si no ingresas uno.

Ingresa el valor a buscar (opcional). Si no ingresas uno, la aplicación usará automáticamente un valor existente en la lista.

Haz clic en Búsqueda Lineal o Búsqueda Binaria.

Los resultados aparecerán en la etiqueta de Resultados, indicando el índice encontrado (si existe) y el tiempo promedio de ejecución en milisegundos.

La gráfica comparará los tiempos promedio de ambos algoritmos en listas de distintos tamaños.
