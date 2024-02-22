"""
Nombre del archivo: Quality_Labels.py
Autor: Guillermo Bellone
Fecha de creación: 5 de noviembre de 2023
Descripción: El codigo superpone la imagen original con la imagen labels, a su vez te muestra las imagenes utilizadas.
Version: 1.0.0
"""

import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
import cv2

def fill_cells(image_np):
    gray = np.array(image_np)
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(3,3))
    res = cv2.morphologyEx(gray,cv2.MORPH_OPEN,kernel)
    return res

# Rutas de las imagenes
ruta_imagen_labels = "C:\\Users\\Leandro\\Leandro\\TRABAJO\\DigPatho\\SEGUNDO DATASET 7056 IMAGENES\\lbl\\lbl_105.png"  # AGREGAR
ruta_imagen_ORG = "C:\\Users\\Leandro\\Leandro\\TRABAJO\\DigPatho\\SEGUNDO DATASET 7056 IMAGENES\\org\\org_105.png"  # AGREGAR

# Abre la imagen
imagen_org = Image.open(ruta_imagen_ORG)
imagen_labels = Image.open(ruta_imagen_labels)

# Convierte la imagen labels a un array numpy
arr_labels = np.array(imagen_labels)

# Invierte los colores de la imagen labels para que sean en escala de grises. (1=200, 2=120, 3=0) Se puede cambiar
arr_invertida = np.where(arr_labels == 1, 200, np.where(arr_labels == 2, 120, 0))

# Crea una nueva imagen a partir del array invertido
imagen_invertida = Image.fromarray(arr_invertida.astype(np.uint8))

# Convierte la imagen invertida a modo RGBA para agregar transparencia
imagen_invertida_rgba = imagen_invertida.convert("RGBA")

# Crea un nuevo canal alfa con el valor 80
nuevo_canal_alfa = Image.new("L", imagen_invertida_rgba.size, 80)

# Mientras mas bajo sea este valor mas transparencia posee la imagen.

# Aplica el nuevo canal alfa a la imagen
imagen_invertida_rgba.putalpha(nuevo_canal_alfa)
imagen_invertida_rgba_rgb = imagen_invertida_rgba.convert("RGB")

# Superpone las imágenes con transparencia al 31%
imagen_resultante = Image.alpha_composite(
    imagen_org.convert("RGBA"), imagen_invertida_rgba
)

# Convierte la imagen resultante a modo RGB para mostrar con Matplotlib
imagen_resultante_rgb = imagen_resultante.convert("RGB")

res = fill_cells(imagen_invertida_rgba_rgb)

# Muestra las imagenes resultante
fig, axs = plt.subplots(1, 3, figsize=(15, 4))

axs[0].imshow(imagen_org)
axs[0].set_title("Original ")
axs[0].axis("off")

axs[1].imshow(imagen_invertida_rgba_rgb)
axs[1].set_title("Labels Escala de grises")
axs[1].axis("off")

axs[2].imshow(res)
axs[2].set_title("Labels Escala de grises - Filtro Aplicado")
axs[2].axis("off")

plt.show()
