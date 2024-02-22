import cv2
import numpy as np
from matplotlib import pyplot as plt
from scipy import ndimage as ndi
from skimage.segmentation import watershed
from skimage.feature import peak_local_max


def watershed_segmentation(image_path):
    # Cargar la imagen
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

    # Definir los valores de píxeles para células benignas, malignas y fondo
    pixel_benigno = 2
    pixel_maligno = 3
    pixel_fondo = 1

    # Generar la máscara de las células benignas y malignas
    mask_benigna = image == pixel_benigno
    mask_maligna = image == pixel_maligno

    # Aplicar la transformación de distancia
    distance = ndi.distance_transform_edt(mask_benigna)

    # Encontrar los máximos locales en la distancia
    coords = peak_local_max(distance, footprint=np.ones((3, 3)), labels=mask_benigna)
    mask = np.zeros(distance.shape, dtype=bool)
    mask[tuple(coords.T)] = True

    # Etiquetar las regiones en la máscara
    markers, _ = ndi.label(mask)

    # Aplicar la segmentación watershed
    labels = watershed(-distance, markers, mask=mask_benigna)

    # Aplicar la transformación de distancia
    distance2 = ndi.distance_transform_edt(mask_maligna)

    # Encontrar los máximos locales en la distancia
    coords2 = peak_local_max(distance2, footprint=np.ones((3, 3)), labels=mask_maligna)
    mask2 = np.zeros(distance2.shape, dtype=bool)
    mask2[tuple(coords2.T)] = True

    # Etiquetar las regiones en la máscara
    markers2, _ = ndi.label(mask2)

    # Aplicar la segmentación watershed
    labels2 = watershed(-distance2, markers2, mask=mask_maligna)

    # Visualizar resultados
    plt.figure(figsize=(10, 5))
    plt.subplot(1, 4, 1)
    plt.imshow(image, cmap="gray")
    plt.title("Imagen Original")

    plt.subplot(1, 4, 2)
    plt.imshow(-distance, cmap="viridis")
    plt.title("Distancia a los máximos locales")

    plt.subplot(1, 4, 3)
    plt.imshow(labels, cmap="viridis")
    plt.title("Células Benignas Segmentadas")

    plt.subplot(1, 4, 4)
    plt.imshow(labels2, cmap="viridis")
    plt.title("Células Malignas Segmentadas")

    plt.show()


if __name__ == "__main__":
    image_path = "c:\\Users\\User\\Desktop\\DIGPATHO\\IMAGENES\\Crudo para segundo entrenamiento ki67\\Imagenes_Trabajadas\\SEGUNDO DATASET 6132 IMAGENES\\lbl\\lbl_59.png"
    watershed_segmentation(image_path)

    # "c:\\Users\\User\\Desktop\\DIGPATHO\\IMAGENES\\Crudo para segundo entrenamiento ki67\\Imagenes_Trabajadas\\SEGUNDO DATASET 6132 IMAGENES\\lbl\\lbl_1.png"
