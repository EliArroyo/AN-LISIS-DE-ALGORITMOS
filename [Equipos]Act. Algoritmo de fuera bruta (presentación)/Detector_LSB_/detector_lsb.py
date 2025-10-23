import cv2
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt 
from scipy import stats
import os
import glob

# ----------------- CLASE DETECTOR Y ANÁLISIS -----------------
class LSBDetector:
    def __init__(self):
        self.image = None
        self.results = {}

    def load_image(self, image_path):
        """Cargar imagen para análisis"""
        try:
            self.image = cv2.imread(image_path)  # Lee la imagen desde el archivo
            if self.image is None:
                raise ValueError("No se pudo cargar la imagen")
            self.image = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)  # Convierte a RGB
            return True
        except Exception as e:
            print(f"Error cargando imagen: {e}")
            return False

    def extraer_mensaje_lsb(self, image_path):
        """Extraer mensaje oculto usando LSB del canal rojo"""
        try:
            if not self.load_image(image_path):
                return None

            canal_rojo = self.image[:, :, 0]  # Selecciona canal rojo
            lsb_bits = []
            height, width = canal_rojo.shape

            # Extrae el bit menos significativo de cada píxel
            for i in range(height):
                for j in range(width):
                    lsb_bits.append(str(canal_rojo[i, j] & 1))

            mensaje_texto = ""
            # Convierte los bits extraídos en caracteres
            for i in range(0, len(lsb_bits), 8):
                byte = lsb_bits[i:i+8]
                if len(byte) < 8:
                    continue
                char_code = int(''.join(byte), 2)
                if 32 <= char_code <= 126:
                    mensaje_texto += chr(char_code)
                else:
                    break
                if mensaje_texto.endswith("END"):
                    return mensaje_texto[:-3]  # Elimina marcador de fin

            return mensaje_texto if mensaje_texto else None

        except Exception as e:
            print(f"Error extrayendo mensaje: {e}")
            return None

    def chi_square_test(self, channel_data):
        """Test Chi-cuadrado para detectar anomalías en LSB"""
        pairs_observed = []
        pairs_expected = []

        # Cuenta pares de valores pares e impares
        for i in range(0, 256, 2):
            if i + 1 < 256:
                even_count = np.sum(channel_data == i)
                odd_count = np.sum(channel_data == i + 1)
                pairs_observed.extend([even_count, odd_count])
                expected = (even_count + odd_count) / 2
                pairs_expected.extend([expected, expected])

        pairs_observed = np.array(pairs_observed)
        pairs_expected = np.array(pairs_expected)
        mask = pairs_expected > 0
        # Calcula estadístico chi-cuadrado
        chi2 = np.sum((pairs_observed[mask] - pairs_expected[mask])**2 / pairs_expected[mask])
        df = len(pairs_observed[mask]) - 1
        p_value = 1 - stats.chi2.cdf(chi2, df) if df > 0 else 1
        return chi2, p_value, df

    def lsb_analysis(self, channel_data):
        # Analiza los bits LSB del canal
        lsb_bits = channel_data & 1
        lsb_stats = {
            'mean': np.mean(lsb_bits),  # Media de los bits LSB
            'variance': np.var(lsb_bits),  # Varianza
            'entropy': self.calculate_entropy(lsb_bits),  # Entropía
            'runs_test': self.runs_test(lsb_bits),  # Prueba de rachas
            'expected_mean': 0.5,
            'expected_variance': 0.25
        }
        return lsb_stats

    def calculate_entropy(self, data):
        # Calcula la entropía de una secuencia binaria
        unique, counts = np.unique(data, return_counts=True)
        probabilities = counts / len(data)
        entropy = -np.sum(probabilities * np.log2(probabilities + 1e-10))
        return entropy

    def runs_test(self, binary_sequence):
        # Prueba de rachas para secuencias binarias
        n = len(binary_sequence)
        if n == 0:
            return 0, 1
        runs = 1
        for i in range(1, n):
            if binary_sequence[i] != binary_sequence[i-1]:
                runs += 1
        ones = np.sum(binary_sequence)
        zeros = n - ones
        if ones == 0 or zeros == 0:
            return runs, 1
        expected_runs = (2 * ones * zeros) / n + 1
        variance_runs = (2 * ones * zeros * (2 * ones * zeros - n)) / (n**2 * (n - 1))
        if variance_runs <= 0:
            return runs, 1
        z_score = (runs - expected_runs) / np.sqrt(variance_runs)
        p_value = 2 * (1 - stats.norm.cdf(abs(z_score)))
        return z_score, p_value

    def spatial_correlation_analysis(self, channel_data):
        # Calcula la correlación horizontal y vertical entre píxeles vecinos
        height, width = channel_data.shape
        horizontal_corr = np.corrcoef(channel_data[:, :-1].flatten(), channel_data[:, 1:].flatten())[0, 1] if width>1 else 0
        vertical_corr = np.corrcoef(channel_data[:-1, :].flatten(), channel_data[1:, :].flatten())[0, 1] if height>1 else 0
        return horizontal_corr, vertical_corr

    def calculate_suspicion_score(self, chi2_p_value, lsb_stats, h_corr, v_corr):
        """Calcula una puntuación de sospecha de 0 a 1 basada en varias pruebas estadísticas."""
        
        # Se definen los pesos para cada prueba. Un peso mayor significa que la prueba es más importante.
        weights = {
            'chi_square': 0.4,
            'mean_deviation': 0.2,
            'entropy': 0.2,
            'correlation': 0.2
        }
        
        score = 0
        
        # 1. Prueba Chi-cuadrado: Un p-valor muy bajo (<0.01) es una fuerte señal de manipulación.
        if chi2_p_value < 0.01:
            score += weights['chi_square']
            
        # 2. Desviación de la media: Si la media de los LSB se aleja mucho de 0.5, es sospechoso.
        mean_deviation = abs(lsb_stats['mean'] - 0.5)
        if mean_deviation > 0.1:
            score += weights['mean_deviation']

       
        if lsb_stats['entropy'] > 0.99:
            score += weights['entropy']
            

        avg_correlation = (abs(h_corr) + abs(v_corr)) / 2
        if avg_correlation < 0.8:
            score += weights['correlation']
            
        return min(score, 1.0)

    def analizar_imagen_completo(self, image_path):
        """Realiza un análisis completo y simplificado, centrado en el canal rojo."""
        print(f"\n🔍 ANÁLISIS COMPLETO DE: {os.path.basename(image_path)}")
        print("="*60)
        if not self.load_image(image_path):
            return
        print(f"Imagen cargada: {self.image.shape}")

        # 1. Intenta extraer un mensaje directamente
        print("\nEXTRACCIÓN DE MENSAJE:")
        mensaje = self.extraer_mensaje_lsb(image_path)
        if mensaje:
            print(f"MENSAJE ENCONTRADO: '{mensaje}'")
        else:
            print("No se encontró mensaje legible")

        # 2. Análisis estadístico enfocado solo en el canal rojo (más eficiente)
        print("\nANÁLISIS (Canal Rojo):")
        
        # Se seleccionan los datos del canal rojo
        channel_data = self.image[:, :, 0]
        flat_data = channel_data.flatten()
        
        # Se realizan todas las pruebas en ese único canal
        chi2, chi2_p_value, df = self.chi_square_test(flat_data)
        lsb_stats = self.lsb_analysis(flat_data)
        h_corr, v_corr = self.spatial_correlation_analysis(channel_data)
        
        # Se calcula una única puntuación de sospecha
        suspicion_score = self.calculate_suspicion_score(chi2_p_value, lsb_stats, h_corr, v_corr)

        # 3. Muestra el resultado final basado en el análisis
        print(f"\nRESULTADO DEL ANÁLISIS:")
        print(f"  Puntuación de sospecha: {suspicion_score:.2f}/1.0")
        
        if mensaje:
            print(f"  Estado: ESTEGANOGRAFÍA DETECTADA")
            print(f"  Mensaje oculto: '{mensaje}'")
        elif suspicion_score > 0.4:
            print(f"  Estado: SOSPECHOSO - Posible esteganografía")
        else:
            print(f"  Estado: NORMAL - No se detectó esteganografía")

# ----------------- CLASE ESTEGANOGRAFÍA -----------------
class EsteganografiaLSB:
    @staticmethod
    def crear_imagen_con_mensaje(mensaje, nombre_archivo="imagen_con_mensaje.png"):
        # Crea una imagen nueva y oculta un mensaje en el canal rojo usando LSB
        try:
            width, height = 200, 200
            imagen = np.random.randint(50, 200, (height, width, 3), dtype=np.uint8)
            mensaje_con_fin = mensaje + "END"
            mensaje_binario = ''.join(format(ord(c), '08b') for c in mensaje_con_fin)
            if len(mensaje_binario) > width * height:
                print("Mensaje demasiado largo")
                return False
            bit_index = 0
            for i in range(height):
                for j in range(width):
                    if bit_index < len(mensaje_binario):
                        imagen[i, j, 0] = (imagen[i, j, 0] & 0xFE) | int(mensaje_binario[bit_index])
                        bit_index += 1
                    else:
                        break
            Image.fromarray(imagen).save(nombre_archivo)
            print(f"Imagen creada: {nombre_archivo}")
            return True
        except Exception as e:
            print(f"Error: {e}")
            return False

    @staticmethod
    def ocultar_mensaje_en_imagen_existente(mensaje, imagen_entrada, imagen_salida="imagen_estego.png"):
        # Oculta un mensaje en una imagen existente usando LSB en el canal rojo
        try:
            imagen = cv2.imread(imagen_entrada)
            if imagen is None:
                print("No se pudo cargar la imagen")
                return False
            imagen = cv2.cvtColor(imagen, cv2.COLOR_BGR2RGB)
            height, width, _ = imagen.shape
            mensaje_con_fin = mensaje + "END"
            mensaje_binario = ''.join(format(ord(c), '08b') for c in mensaje_con_fin)
            if len(mensaje_binario) > width * height:
                print("Mensaje demasiado largo")
                return False
            bit_index = 0
            for i in range(height):
                for j in range(width):
                    if bit_index < len(mensaje_binario):
                        imagen[i, j, 0] = (imagen[i, j, 0] & 0xFE) | int(mensaje_binario[bit_index])
                        bit_index += 1
                    else:
                        break
            Image.fromarray(imagen).save(imagen_salida)
            print(f"Mensaje oculto en: {imagen_salida}")
            return True
        except Exception as e:
            print(f"Error: {e}")
            return False

# ----------------- MENÚ -----------------
def mostrar_menu():
    # Muestra el menú principal
    print("\n" + "="*60)
    print(" DETECTOR DE MSJS OCULTOS (LSB) ")
    print("="*60)
    print("1. Analizar imagen")
    print("2. Crear imagen con esteganografía (nueva)")
    print("3. Ocultar mensaje en imagen existente")
    print("4. Salir")
    print("="*60)

def seleccionar_imagen():
    # Permite al usuario seleccionar una imagen del directorio actual
    extensiones = ['*.jpg', '*.jpeg', '*.png', '*.bmp', '*.tiff']
    imagenes = []
    for ext in extensiones:
        imagenes.extend(glob.glob(ext))
    imagenes = list(dict.fromkeys([img.lower() for img in imagenes]))
    if not imagenes:
        print(" No se encontraron imágenes en el directorio actual")
        return None
    print("\nImágenes encontradas:")
    for i, img in enumerate(imagenes, 1):
        print(f"  {i}. {img}")
    try:
        opcion = int(input(f"\nSelecciona una imagen (1-{len(imagenes)}): "))
        if 1 <= opcion <= len(imagenes):
            return imagenes[opcion - 1]
        else:
            print("Opción no válida")
            return None
    except ValueError:
        print("Por favor ingresa un número válido")
        return None

def main():
    # Función principal del programa
    detector = LSBDetector()
    esteganografia = EsteganografiaLSB()
    while True:
        mostrar_menu()
        opcion = input("Selecciona una opción: ").strip()
        if opcion == '1':
            imagen_path = seleccionar_imagen()
            if imagen_path:
                detector.analizar_imagen_completo(imagen_path)
                input("\nPresiona Enter para continuar...")
        elif opcion == '2':
            mensaje = input("\nIngresa el mensaje que desea ocultar: ").strip()
            if mensaje:
                nombre_archivo = input("Nombre del archivo (default: imagen_con_mensaje.png): ").strip()
                if not nombre_archivo: nombre_archivo = "imagen_con_mensaje.png"
                if not nombre_archivo.lower().endswith(('.png', '.jpg', '.jpeg')):
                    nombre_archivo += '.png'
                esteganografia.crear_imagen_con_mensaje(mensaje, nombre_archivo)
            input("\nPresiona Enter para continuar...")
        elif opcion == '3':
            imagen_path = seleccionar_imagen()
            if imagen_path:
                mensaje = input("\nIngresa el mensaje que desea ocultar: ").strip()
                if mensaje:
                    nombre_archivo = input("Nombre del archivo de salida (default: imagen_estego.png): ").strip()
                    if not nombre_archivo: nombre_archivo1 = "imagen_estego.png"
                    if not nombre_archivo.lower().endswith(('.png', '.jpg', '.jpeg')):
                        nombre_archivo += '.png'
                    esteganografia.ocultar_mensaje_en_imagen_existente(mensaje, imagen_path, nombre_archivo)
            input("\nPresiona Enter para continuar...")
        elif opcion == '4':
            print("\nPrograma Finalizado :)")
            break
        else:
            print("Opción no valida. Por favor selecciona 1-4.")
            input("Presiona Enter para continuar...")

if __name__ == "__main__":
    print("Iniciando Detector...")
    main()