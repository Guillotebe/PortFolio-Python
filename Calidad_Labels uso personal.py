import matplotlib.pyplot as plt
import numpy as np
from PIL import Image

# Ruta de la imagen PNG
ruta_imagen_ORG = "c:\\Users\\User\\Desktop\\DIGPATHO\\IMAGENES\\Crudo para segundo entrenamiento ki67\\Imagenes_Trabajadas\\SEGUNDO DATASET 6132 IMAGENES\\org\\org_1.png"
ruta_imagen_labels = "c:\\Users\\User\\Desktop\\DIGPATHO\\IMAGENES\\Crudo para segundo entrenamiento ki67\\Imagenes_Trabajadas\\SEGUNDO DATASET 6132 IMAGENES\\lbl\\lbl_1.png"

# Abre la imagen
imagen_org = Image.open(ruta_imagen_ORG)
imagen_labels = Image.open(ruta_imagen_labels)

# Muestra las imagenes
# plt.imshow(imagen_labels)
# plt.title("Imagen con 3 etiquetas")
# plt.show()
# plt.imshow(imagen_org)
# plt.title("Imagen original")
# plt.show()

# Convierte la imagen labels a un array numpy
# arr_labels = plt.imread(ruta_imagen_labels)

# # Crea una paleta de colores basada en los valores únicos en la imagen labels
# colores = {1: "red", 2: "green", 3: "blue"}
# cmap = ListedColormap(list(colores.values()))

# # Grafica la imagen con la barra de colores
# plt.imshow(arr_labels, cmap=cmap)
# plt.colorbar(ticks=[1, 2, 3], label="Valores", orientation="horizontal")
# plt.title("Imagen de Labels con Barra de Colores")
# plt.show()

# # Muestra la barra de colores
# plt.show()

# 1: Fondo 2: Cel Benignas 3: Cel malignas.

# LO DE ARRIBA FUNCIONA

# Convierte la imagen labels a un array numpy
arr_labels = np.array(imagen_labels)

# Invierte los colores de la imagen labels
arr_invertida = np.where(arr_labels == 1, 200, np.where(arr_labels == 2, 120, 0))

# Crea una nueva imagen a partir del array invertido
imagen_invertida = Image.fromarray(arr_invertida.astype(np.uint8))

# Convierte la imagen invertida a modo RGBA para agregar transparencia
imagen_invertida_rgba = imagen_invertida.convert("RGBA")

# Crea un nuevo canal alfa con el valor 80
nuevo_canal_alfa = Image.new("L", imagen_invertida_rgba.size, 80)

# Aplica el nuevo canal alfa a la imagen
imagen_invertida_rgba.putalpha(nuevo_canal_alfa)
imagen_invertida_rgba_rgb = imagen_invertida_rgba.convert("RGB")
# Superpone las imágenes con transparencia al 31%
imagen_resultante = Image.alpha_composite(
    imagen_org.convert("RGBA"), imagen_invertida_rgba
)

# Convierte la imagen resultante a modo RGB para mostrar con Matplotlib
imagen_resultante_rgb = imagen_resultante.convert("RGB")

# Muestra la imagen resultante

# Muestra las imágenes
fig, axs = plt.subplots(1, 4, figsize=(15, 4))

axs[0].imshow(imagen_org)
axs[0].set_title("Original ")
axs[0].axis("off")

axs[3].imshow(imagen_labels)
axs[3].set_title("Labels sin tratar")
axs[3].axis("off")

axs[2].imshow(imagen_invertida_rgba_rgb)
axs[2].set_title("Labels Escala de grises")
axs[2].axis("off")

axs[1].imshow(imagen_resultante_rgb)
axs[1].set_title("Imagenes superpuestas")
axs[1].axis("off")

plt.show()
