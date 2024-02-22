"""
HERRAMIENTA DE DESARROLLO
Nombre del archivo: Quality_Labels.py
Autor: Guillermo Bellone
Fecha de creación: 5 de noviembre de 2023
Descripción: El codigo superpone la imagen original con la imagen labels, a su vez te muestra las imagenes utilizadas.
Version: 1.0.0
HERRAMIENTA DE DESARROLLO
"""

import matplotlib.pyplot as plt
import numpy as np
from PIL import Image

# Rutas de las imagenes
ruta_imagen_ORG = "RUTA"  # AGREGAR
ruta_imagen_labels = "RUTA"  # AGREGAR

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

# Muestra las imagenes resultante
fig, axs = plt.subplots(2, 2, figsize=(15, 4))

axs[0, 0].imshow(imagen_org)
axs[0, 0].set_title("Original ")
axs[0, 0].axis("off")

axs[0, 1].imshow(imagen_labels)
axs[0, 1].set_title("Labels sin tratar")
axs[0, 1].axis("off")

axs[1, 0].imshow(imagen_invertida_rgba_rgb)
axs[1, 0].set_title("Labels Escala de grises")
axs[1, 0].axis("off")

axs[1, 1].imshow(imagen_resultante_rgb)
axs[1, 1].set_title("Imagenes superpuestas")
axs[1, 1].axis("off")

plt.show()
