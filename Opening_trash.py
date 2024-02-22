import cv2
import numpy as np
import matplotlib.pyplot as plt


def labels_to_gray(labels_image):
    # Cambiar valores (255 = positivo, 200 = negativo, 0 = fondo)
    labels_image[labels_image == 3] = 0
    labels_image[labels_image == 2] = 120
    labels_image[labels_image == 1] = 200


def morphological_opening(image, kernel_shape):
    kernel = np.ones(kernel_shape, dtype=np.uint8)
    """ kernel = np.array([[0, 1, 0],
                       [1, 1, 1],
                       [0, 1, 0]], dtype=np.uint8) """

    opening = cv2.morphologyEx(image, cv2.MORPH_OPEN, kernel)
    return opening


def display_results(
    original_labels,
    processed_labels,
    original_positive,
    processed_positive,
    original_negative,
    processed_negative,
):
    # Imagen Completa
    # Imagen de labels original, fila 1 columna 1
    plt.subplot(3, 2, 1)
    plt.title("Labels sin procesar")
    plt.imshow(original_labels)

    # Opening final, fila 1 columna 2
    plt.subplot(3, 2, 2)
    plt.title("Labels procesada")
    plt.imshow(processed_labels)

    # Malignas
    # Celulas positives sin procesar, fila 2 columna 1
    plt.subplot(3, 2, 3)
    plt.title("Malignas sin procesar")
    plt.imshow(original_positive)

    # Celulas positives procesada, fila 2 columna 2
    plt.subplot(3, 2, 4)
    plt.title("Malignas procesada")
    plt.imshow(processed_positive)

    # Benignas
    # Celulas negatives sin procesar, fila 3 columna 1
    plt.subplot(3, 2, 5)
    plt.title("Benignas sin procesar")
    plt.imshow(original_negative)

    # Celulas negatives procesadas, fila 3 columna 2
    plt.subplot(3, 2, 6)
    plt.title("Benignas procesada")
    plt.imshow(processed_negative)

    # Ajustar el diseño para evitar superposiciones
    plt.tight_layout()

    # Mostrar el plot
    plt.show()


def opening(labels_image):
    # Llevar imagen de labels a escala de grises, la original tiene valores 0, 1 y 2
    labels_to_gray(labels_image)

    # Operación Morfologica

    # Imagen binaria celulas malignas
    positives = labels_image.copy()
    positives[positives != 0] = 200  # Obtengo la imagen binaria de celulas positives
    positives_opening = morphological_opening(
        positives, (7, 7)
    )  # Imagen resultante de la operación

    # Imagen binaria celulas benignas
    negatives = labels_image.copy()
    negatives[
        negatives != 120
    ] = 255  # Las celulas negatives valen 200 en escala de grises, el resto fondo
    negatives[negatives == 120] = 0  # Llevo a blanco el gris
    negatives_opening = morphological_opening(
        negatives, (7, 7)
    )  # Imagen resultante de la operación

    # Ajuste a gris de las celulas benignas
    negatives_opening[negatives_opening == 0] = 120

    # Resultado conjunto de las 2 operaciones
    final_opening = negatives_opening + positives_opening

    # Visualización de las imagenes
    display_results(
        labels_image,
        final_opening,
        positives,
        positives_opening,
        negatives,
        negatives_opening,
    )

    # Devolver imagen con la operación morfologica realizada
    # return final_opening
