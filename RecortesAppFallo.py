# Nombre del archivo: RecortesAppFallo.py
# Autor: Guillermo Bellone
# Fecha de creación: 20 de Diciembre de 2023
# Descripción: Recorta una imagen, pero en este caso lo resuelve mal xq amplia demasiado la imagen. Fue descartado el modelo
# version: 1.0.0


import cv2
import numpy as np
from matplotlib import pyplot as plt


def ajustar_tamano_multiplo_256(imagen):
    alto, ancho, _ = imagen.shape

    # Calcular el nuevo tamaño que sea múltiplo de 256
    nuevo_ancho = ((ancho - 1) // 256 + 1) * 256
    nuevo_alto = ((alto - 1) // 256 + 1) * 256

    pixeles_extra_ancho = nuevo_ancho - ancho
    pixeles_extra_alto = nuevo_alto - alto

    # Agregar píxeles azules a la imagen original
    imagen_original_ampliada = np.zeros((nuevo_alto, nuevo_ancho, 3), dtype=np.uint8)
    imagen_original_ampliada[:alto, :ancho] = imagen

    # Dividir la imagen en trozos de 256x256
    trozos, filas, columnas = dividir_en_trozos(imagen_original_ampliada, 256)

    return trozos, filas, columnas, alto, ancho, pixeles_extra_ancho, pixeles_extra_alto


def dividir_en_trozos(imagen, tamano_trozo):
    alto, ancho, _ = imagen.shape
    trozos = []

    filas = 0
    columnas = 0

    for y in range(0, alto, tamano_trozo):
        filas += 1
        for x in range(0, ancho, tamano_trozo):
            if filas == 1:
                columnas += 1
            trozo = imagen[y : y + tamano_trozo, x : x + tamano_trozo]
            trozos.append(trozo)

    return trozos, filas, columnas


# EN ESTA FUNCION NO DEBERIA UTILIZAR TROZOS SI NO LO QUE DEVUELVE LA IA
def rearmar_imagen(trozos, filas, columnas, alto_org, ancho_org):
    tamano_trozo = trozos[0].shape[
        0
    ]  # Tamaño de un trozo (suponemos que todos tienen el mismo tamaño)
    alto = filas * tamano_trozo
    ancho = columnas * tamano_trozo

    imagen_resultante = np.zeros((alto, ancho, 3), dtype=np.uint8)

    indice = 0
    for i in range(filas):
        for j in range(columnas):
            imagen_resultante[
                i * tamano_trozo : (i + 1) * tamano_trozo,
                j * tamano_trozo : (j + 1) * tamano_trozo,
            ] = trozos[indice]
            indice += 1

    x, y, ancho, alto = 0, 0, ancho_org, alto_org
    lbl_tamaño_orginal = cv2.getRectSubPix(
        imagen_resultante, (ancho, alto), (x + ancho / 2, y + alto / 2)
    )
    return lbl_tamaño_orginal


# Es de 2585x1792, deberia quedar de 4096x2048, 16 en filas y 8 en columnas, 16x8 = 128 recortes en total
# ruta_imagen = "F:\\grabaciones\\Crudo para segundo entrenamiento ki67\\Hosp ezeiza\\CASO 1\\1699063435546 ESTAAAAAAAA LISTA.jpg"  # Cambia esto por la ruta de tu imagen
# Es de 640x480, deberia quedar de 1024x512, 4 en filas y 2 en columnas, 4x2 = 8 recortes en total
# ruta_imagen = "F:\\grabaciones\\Crudo para segundo entrenamiento ki67\\Hosp Oulton\\Muestra 3\\OU 023.jpg"
# Es de 200x200, deberia quedar una sola de 256x256
ruta_imagen = "c:\\Users\\User\\Desktop\\PRUEBA\\imagen completa\\Prueba2.jpg"
imagen_original = cv2.imread(ruta_imagen)
(
    trozos_resultantes,
    filas,
    columnas,
    alto,
    ancho,
    pixel_extra_ancho,
    pixel_extra_alto,
) = ajustar_tamano_multiplo_256(imagen_original)

# Mostrar o guardar los trozos resultantes, según sea necesario
for i, trozo in enumerate(trozos_resultantes):
    print(trozo.shape, i)

# ANALISIS DE IA


# Rearmar la imagen
imagen_rearmada = rearmar_imagen(trozos_resultantes, filas, columnas, alto, ancho)

# Mostrar o guardar la imagen rearmada, según sea necesario
cv2.imshow("Imagen Rearmada", imagen_rearmada)
cv2.waitKey(0)
cv2.destroyAllWindows()
