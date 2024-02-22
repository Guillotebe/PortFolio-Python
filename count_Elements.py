"""
Nombre del archivo: count_Elements.py
Autor: Guillermo Bellone
Fecha de creación: 17 de Diciembre de 2023
Descripción: El codigo cuenta los elementos de la imagen labels y realiza el promedio de las celulas malignas por sobre el total y las visualiza en la original.
Version: 1.0.0
"""
import cv2
import numpy as np
from skimage.measure import label, regionprops
import matplotlib.pyplot as plt


def contar_celulas(imagen_clasificada):
    # Etiqueta y cuenta los componentes conectados en la imagen
    etiquetada = label(imagen_clasificada, connectivity=2)
    propiedades = regionprops(etiquetada, intensity_image=imagen_clasificada)

    # Inicializa el contador de células malignas y benignas
    celulas_malignas = 0
    celulas_benignas = 0

    # Itera sobre las regiones identificadas
    for region in propiedades:
        etiqueta = region.label
        area = region.area

        # Verifica si la región es una célula maligna (etiqueta 3)
        if np.any(region.intensity_image == 3):
            celulas_malignas += 1
        # Verifica si la región es una célula benigna (etiqueta 2)
        elif np.any(region.intensity_image == 2):
            celulas_benignas += 1

    # Calcula el porcentaje de células malignas
    total_celulas = celulas_malignas + celulas_benignas
    porcentaje_malignas = (
        (celulas_malignas / total_celulas) * 100 if total_celulas > 0 else 0
    )

    return celulas_malignas, celulas_benignas, porcentaje_malignas


def marcar_celulas(imagen_original, imagen_clasificada):
    # Etiqueta y cuenta los componentes conectados en la imagen
    etiquetada = label(imagen_clasificada, connectivity=2)
    propiedades = regionprops(etiquetada, intensity_image=imagen_clasificada)

    # Crea una copia de la imagen original para marcar las células
    imagen_marcada = np.copy(imagen_original)

    # Lista para almacenar las etiquetas de células malignas
    etiquetas_malignas = []

    # Itera sobre las regiones identificadas
    for region in propiedades:
        etiqueta = region.label

        # Verifica si la región es una célula maligna (etiqueta 3)
        if np.any(region.intensity_image == 3):
            coords = region.coords.T
            imagen_marcada[coords[0], coords[1]] = [0, 0, 255]  # Rojo

            # Marcar elementos alrededor como fondo (etiqueta 1)
            for i in range(
                max(0, region.bbox[0] - 1),
                min(imagen_clasificada.shape[0], region.bbox[2] + 1),
            ):
                for j in range(
                    max(0, region.bbox[1] - 1),
                    min(imagen_clasificada.shape[1], region.bbox[3] + 1),
                ):
                    if etiquetada[i, j] != etiqueta:
                        imagen_clasificada[i, j] = 1

            etiquetas_malignas.append(etiqueta)

    # Itera nuevamente para marcar las células benignas (etiqueta 2) solo si no hay superposición con células malignas
    for region in propiedades:
        etiqueta = region.label

        # Verifica si la región es una célula benigna (etiqueta 2) y no está superpuesta con células malignas
        if np.any(region.intensity_image == 2) and etiqueta not in etiquetas_malignas:
            coords = region.coords.T
            imagen_marcada[coords[0], coords[1]] = [255, 0, 0]  # Azul

    return imagen_marcada


# Ruta de la imagen original
ruta_imagen_original = "RUTA"  # AGREGAR
imagen_original = cv2.imread(ruta_imagen_original)

# Ruta de la imagen clasificada (resultado del tercer código)
ruta_imagen_clasificada = "RUTA"  # AGREGAR
imagen_clasificada = cv2.imread(ruta_imagen_clasificada, cv2.IMREAD_GRAYSCALE)

# Llama a la función para marcar células
imagen_marcada = marcar_celulas(imagen_original, imagen_clasificada)

# Llama a la función para contar células
celulas_malignas, celulas_benignas, porcentaje_malignas = contar_celulas(
    imagen_clasificada
)
# Imprime los resultados
print(f"Número de células malignas: {celulas_malignas}")
print(f"Número de células benignas: {celulas_benignas}")
print(f"Porcentaje de células malignas: {porcentaje_malignas:.2f}%")

# Muestra la imagen original con células marcadas
plt.imshow(cv2.cvtColor(imagen_marcada, cv2.COLOR_BGR2RGB))
plt.title("Células Marcadas")
plt.show()
