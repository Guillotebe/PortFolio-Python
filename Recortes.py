# Nombre del archivo: Recortes.py
# Autor: Guillermo Bellone
# Fecha de creación: 20 de Diciembre de 2023
# Descripción: Codigo que carga dos carpetas de imagenes y las recorta en tamaño 256x256. en caso de que no lleguen a recortalas de manera completa toma porciones que ya fue utilizada.
# version: 1.0.0

import cv2
import os
import numpy as np


def redimensionar_y_recortar(
    ruta_imagen_original, ruta_imagen_labels, ruta_destino, tamano_objetivo=256
):
    # Cargar la imagen original
    imagen_original = cv2.imread(ruta_imagen_original)

    # Cargar la imagen de etiquetas
    imagen_labels = cv2.imread(ruta_imagen_labels, cv2.IMREAD_GRAYSCALE)

    # fijo un tamaño minimo de la imagen para hacer la reduccion al 50%
    tamaño_minimo = 256 * 2

    # Verificar si la imagen original es menor que el tamaño objetivo
    if imagen_original.shape[0] < (tamaño_minimo) or imagen_original.shape[1] < (
        tamaño_minimo
    ):
        # Usar la imagen original sin redimensionar
        imagen_original_redimensionada = imagen_original
        imagen_labels_redimensionada = imagen_labels
        nuevo_ancho = imagen_original.shape[0]
        nuevo_alto = imagen_original.shape[1]
    else:
        # Downsampling a un factor de 0.5
        imagen_original_downsampled = cv2.resize(imagen_original, None, fx=0.5, fy=0.5)
        imagen_labels_downsampled = cv2.resize(
            imagen_labels, None, fx=0.5, fy=0.5, interpolation=cv2.INTER_NEAREST
        )

        # Obtener las dimensiones originales de la imagen downsampling
        alto_downsampled, ancho_downsampled = imagen_original_downsampled.shape[:2]

        # Calcular el nuevo tamaño proporcional manteniendo la relación de aspecto
        nuevo_ancho = tamano_objetivo * round(ancho_downsampled / tamano_objetivo)
        nuevo_alto = int(alto_downsampled * (nuevo_ancho / ancho_downsampled))

        # Redimensionar la imagen downsampling
        imagen_original_redimensionada = cv2.resize(
            imagen_original_downsampled, (nuevo_ancho, nuevo_alto)
        )
        imagen_labels_redimensionada = cv2.resize(
            imagen_labels_downsampled,
            (nuevo_ancho, nuevo_alto),
            interpolation=cv2.INTER_NEAREST,
        )

    # Carpeta para todas las imágenes originales
    carpeta_original = "originales"
    ruta_destino_original = os.path.join(ruta_destino, carpeta_original)
    if not os.path.exists(ruta_destino_original):
        os.makedirs(ruta_destino_original)

    # Carpeta para todas las etiquetas
    carpeta_labels = "labels"
    ruta_destino_labels = os.path.join(ruta_destino, carpeta_labels)
    if not os.path.exists(ruta_destino_labels):
        os.makedirs(ruta_destino_labels)

    # Recortar la imagen downsampling en fragmentos de 256x256
    for y in range(0, nuevo_alto, tamano_objetivo):
        for x in range(0, nuevo_ancho, tamano_objetivo):
            # Obtener el fragmento desde la imagen downsampling
            fragmento_original = imagen_original_redimensionada[
                y : y + tamano_objetivo, x : x + tamano_objetivo
            ]
            fragmento_labels = imagen_labels_redimensionada[
                y : y + tamano_objetivo, x : x + tamano_objetivo
            ]

            # Completar con porciones cercanas de la imagen downsampling
            if fragmento_original.shape[0] < tamano_objetivo:
                diferencia = tamano_objetivo - fragmento_original.shape[0]
                complemento_original = imagen_original_redimensionada[
                    y - diferencia : y, x : x + tamano_objetivo
                ]
                complemento_labels = imagen_labels_redimensionada[
                    y - diferencia : y, x : x + tamano_objetivo
                ]
                fragmento_original = np.vstack(
                    [complemento_original, fragmento_original]
                )
                fragmento_labels = np.vstack([complemento_labels, fragmento_labels])

            if fragmento_original.shape[1] < tamano_objetivo:
                diferencia = tamano_objetivo - fragmento_original.shape[1]
                complemento_original = imagen_original_redimensionada[
                    y : y + tamano_objetivo, x - diferencia : x
                ]
                complemento_labels = imagen_labels_redimensionada[
                    y : y + tamano_objetivo, x - diferencia : x
                ]
                fragmento_original = np.hstack(
                    [complemento_original, fragmento_original]
                )
                fragmento_labels = np.hstack([complemento_labels, fragmento_labels])

            # Contador para numerar las imágenes
            contador = len(os.listdir(ruta_destino_original)) + 1

            # Guardar los fragmentos en las carpetas de destino
            nombre_fragmento_org = f"org_{contador}.png"
            nombre_fragmento_labels = f"lbl_{contador}.png"

            # Rutas de destino específicas para todas las originales y labels
            ruta_guardado_org = os.path.join(
                ruta_destino_original, nombre_fragmento_org
            )
            ruta_guardado_labels = os.path.join(
                ruta_destino_labels, nombre_fragmento_labels
            )
            if (
                fragmento_original.shape[0] == 256
                and fragmento_original.shape[1] == 256
            ):
                cv2.imwrite(ruta_guardado_org, fragmento_original)
                cv2.imwrite(ruta_guardado_labels, fragmento_labels)


# Rutas de las carpetas que contienen las imágenes originales y de etiquetas
carpeta_originales = "PATH ORIGINALES"  # AGREGAR
carpeta_labels = "PATH LABELS"  # AGREGAR

# Carpeta de destino para los fragmentos
carpeta_destino = "PATH DESTINO"  # AGREGAR

# Obtener la lista de archivos en las carpetas originales y labels
archivos_originales = sorted(
    [f for f in os.listdir(carpeta_originales) if f.startswith("org_")]
)
archivos_labels = sorted(
    [f for f in os.listdir(carpeta_labels) if f.startswith("lbl_")]
)

# Verificar que haya la misma cantidad de archivos en ambas carpetas
if len(archivos_originales) != len(archivos_labels):
    print(
        "Error: La cantidad de archivos en las carpetas originales y labels no coincide."
    )
else:
    # Iterar sobre los pares de archivos
    for i, (archivo_original, archivo_labels) in enumerate(
        zip(archivos_originales, archivos_labels), 1
    ):
        ruta_original = os.path.join(carpeta_originales, archivo_original)
        ruta_labels = os.path.join(carpeta_labels, archivo_labels)

        # Crear una carpeta específica para cada par de imágenes
        carpeta_resultados = os.path.join(carpeta_destino, f"resultado_{i}")
        os.makedirs(carpeta_resultados, exist_ok=True)

        # Llamar a la función para redimensionar y recortar
        redimensionar_y_recortar(ruta_original, ruta_labels, carpeta_resultados)
