"""
Nombre del archivo: preprocesamiento.py
Autor: Guillermo Bellone
Fecha de creación: 5 de noviembre de 2023
Descripción: uavizado, rellenado de huecos y eliminacion de las celulas benignas al rededor de las malignas.
Version: 1.0.0
"""

import cv2
import numpy as np
import matplotlib.pyplot as plt


def rellenar_huecos(image_np):
    # Convertir la imagen a escala de grises si no lo está
    gray = (
        cv2.cvtColor(image_np, cv2.COLOR_BGR2GRAY)
        if len(image_np.shape) == 3
        else image_np
    )

    # Aplicar un filtro gaussiano
    blurred = cv2.GaussianBlur(gray, (5, 5), 1)

    # Aplicar una operación de apertura morfológica para rellenar huecos
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
    res = cv2.morphologyEx(blurred, cv2.MORPH_OPEN, kernel)

    return res


def completar_con_fondo_alrededor_malignas(image_np, labels, distancia_fondo):
    # Crear una máscara de las células malignas
    mask_celulas_malignas = (labels == 3).astype(np.uint8)

    # Aplicar una operación de dilatación alrededor de las células malignas
    kernel = np.ones((distancia_fondo, distancia_fondo), np.uint8)
    mask_dilatada = cv2.dilate(mask_celulas_malignas, kernel, iterations=1)

    # Crear una máscara combinada para incluir tanto las células malignas como las benignas
    mask_malignas_benignas = np.logical_or(mask_celulas_malignas, (labels == 2)).astype(
        np.uint8
    )

    # Aplicar una operación AND con la máscara dilatada para incluir el reborde alrededor de las células malignas
    mask_final = cv2.bitwise_and(mask_malignas_benignas, mask_dilatada)

    # Crear una imagen de fondo
    background = np.zeros_like(image_np)  # Inicializar con fondo blanco

    # Copiar la imagen original en el fondo donde no hay dilatación
    background[mask_final == 0] = image_np[mask_final == 0]

    return background


# Ruta de la imagen de etiquetas
ruta_imagen_labels = "c:\\Users\\User\\Desktop\\PRUEBA1.png"
ruta_imagen_org = "c:\\Users\\User\\Desktop\\ORG1.jpg"

# Cargar la imagen de etiquetas
imagen_etiquetas = cv2.imread(ruta_imagen_labels, cv2.IMREAD_GRAYSCALE)
imagen_original = cv2.imread(ruta_imagen_org)

# Verificar si la carga de la imagen fue exitosa
if imagen_etiquetas is None:
    print(
        "Error al cargar la imagen de etiquetas. Verifica la ruta y el formato del archivo."
    )
else:
    # Aplicar un filtro gaussiano con un kernel de tamaño 5x5 y sigma de 1
    imagen_suavizada = cv2.GaussianBlur(imagen_etiquetas, (5, 5), 1)
    imagen_suavizada2 = cv2.GaussianBlur(imagen_suavizada, (5, 5), 1)
    imagen_suavizada3 = cv2.GaussianBlur(imagen_suavizada2, (5, 5), 1)
    imagen_suavizada4 = cv2.GaussianBlur(imagen_suavizada3, (5, 5), 1)
    # Rellenar huecos en células benignas (etiqueta 2)
    imagen_rellena = rellenar_huecos(imagen_suavizada4)

    # Crear un borde alrededor de las células benignas
    borde_celulas_benignas = completar_con_fondo_alrededor_malignas(
        imagen_rellena, imagen_rellena, 6
    )

    # Muestra la imagen original, la imagen suavizada, la imagen rellena, el borde alrededor de las células benignas y la imagen final
    plt.subplot(2, 3, 1)
    plt.title("Imagen Original")
    plt.imshow(imagen_original)

    plt.subplot(2, 3, 2)
    plt.title("Imagen labels")
    plt.imshow(imagen_etiquetas, cmap="viridis")

    plt.subplot(2, 3, 3)
    plt.title("Imagen suavizada")
    plt.imshow(imagen_suavizada, cmap="viridis")

    plt.subplot(2, 3, 4)
    plt.title("Células Rellena")
    plt.imshow(imagen_rellena, cmap="viridis")

    plt.subplot(2, 3, 5)
    plt.title("Dilatación alrededor de Células Malignas")
    plt.imshow(borde_celulas_benignas, cmap="viridis")

    plt.show()
