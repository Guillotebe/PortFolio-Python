"""
HERRAMIENTA DE DESARROLLO
Nombre del archivo: Transform_to_labels.py
Autor: Guillermo Bellone
Fecha de creación: 5 de Noviembre de 2023
Descripción: El codigo toma la imagen Trabajada por Qu-Path, y te la transforma en 1, 2 y 3.
1: Fondo
2: Celula benigna (azul)
3: Celula maligna (rojo)

Version: 1.0.0
NOTAS: REVISAR TOMA DE COLORES, y RUTAS
HERRAMIENTA DE DESARROLLO
"""

import cv2
import numpy as np
import matplotlib.pyplot as plt


# Función para clasificar los píxeles
def clasificar_pixeles(img):
    # Define los rangos de colores en formato BGR (OpenCV)
    rojo_bajo = np.array(
        [0, 0, 100]
    )  # Se cambia el valor para tener un umbral mas bajo de rojo (Ronda entre los 80 y 120)
    rojo_alto = np.array(
        [130, 130, 255]
    )  # Se cambian los valores que no son rojo para mejorar adquisicion del color (Rondan entre los 130 y 170)

    azul_bajo = np.array(
        [120, 0, 0]
    )  # Se cambia el valor para tener un umbral mas bajo de azul (Ronda entre los 80 y 120)
    azul_alto = np.array(
        [255, 140, 140]
    )  # Se cambian los valores que no son azul para mejorar adquisicion del color (Rondan entre los 130 y 170)

    # PD: Estos rangos deberian poder variarse devido a que las imagenes poseen iluminaciones diferentes.

    # Crea máscaras para los píxeles rojos y azules
    mascara_roja = cv2.inRange(img, rojo_bajo, rojo_alto)
    mascara_azul = cv2.inRange(img, azul_bajo, azul_alto)

    # Inicializa la imagen clasificada con píxeles de fondo
    img_clasificada = np.ones_like(mascara_roja, dtype=np.uint8)

    # Asigna etiquetas a los píxeles según la máscara
    img_clasificada[mascara_roja > 0] = 3  # Píxeles rojos
    img_clasificada[mascara_azul > 0] = 2  # Píxeles azules

    return img_clasificada


# Carga la imagen de entrada
rutaimagen = "C:\\Users\\User\\Desktop\\DIGPATHO\\IMAGENES\\A SUBIR\\QUPATH\\org_65.jpg"  # AGREGARSS
imagen_entrada = cv2.imread(rutaimagen)

# Clasifica los píxeles
imagen_clasificada = clasificar_pixeles(imagen_entrada)

# Visualiza la imagen clasificada
plt.imshow(imagen_clasificada)  # Puedes cambiar el cmap según tu preferencia
plt.title("Imagen Clasificada")
plt.show()

# Pregunta al usuario si desea guardar la imagen clasificada
guardar = input("¿Desea guardar la imagen clasificada? (S/N): ")

if guardar.lower() == "s":
    # Guarda la imagen clasificada
    ruta_guardado = "C:\\Users\\User\\Desktop\\DIGPATHO\\IMAGENES\\A SUBIR\\LABELS\\lbl_65.jpg"  # Agregar ruta de guardado
    cv2.imwrite(ruta_guardado, imagen_clasificada)
    print(f"Imagen guardada en: {ruta_guardado}")
else:
    print("Imagen no guardada.")
    plt.close()  # Cierra la ventana de visualización si no se va a guardar la imagen
