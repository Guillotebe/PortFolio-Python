# Nombre del archivo: change_Labels.py
# Autor: Guillermo Bellone
# Fecha de creación: 20 de Noviembre de 2023
# Descripción: Codigo que abre la imagen y al hacer click cambia los labels de las imagenes, de 2 a 3 y de 3 a 2 (de beningo a maligno y viceversa)
# si precionamos en el findo no realizaria ninguna funcion.
# version: 1.0.0
# Notas: La imagen NO se guarda una vez realizado el cambio, es solo la funcion.
import cv2
import matplotlib.pyplot as plt


# Funcion para obtener el color del pixel una vez realizado el click
def obtener_color(event):
    if event.xdata and event.ydata:
        x = int(event.xdata)
        y = int(event.ydata)
        label_actual = imagen[y, x]

        # Cambiar etiquetas de los vecinos
        cambiar_etiquetas(x, y, label_actual)

        # Imprimir información después del cambio
        print("Coordenadas:", x, y)
        print("Valor del píxel antes del cambio:", label_actual)
        print("Nueva imagen:")
        print(imagen)

        # Mostrar la nueva imagen
        ax.imshow(imagen, cmap="gray")
        plt.draw()


# Funcion para cambio de etiqueta del pixel y los de al rededor una vez realizado el click
def cambiar_etiquetas(x, y, label_actual):
    # Cambiar etiqueta actual
    if imagen[y, x] == 3:
        imagen[y, x] = 2
    elif imagen[y, x] == 2:
        imagen[y, x] = 3

    # Buscar vecinos con la misma etiqueta y cambiarlos también (recursividad)
    for i in range(max(0, y - 1), min(imagen.shape[0], y + 2)):
        for j in range(max(0, x - 1), min(imagen.shape[1], x + 2)):
            if imagen[i, j] == label_actual:
                cambiar_etiquetas(j, i, label_actual)


# Ruta de la imagen
ruta_imagen = "C:\\Users\\User\\Desktop\\DIGPATHO\\IMAGENES\\Crudo para segundo entrenamiento ki67\\Imagenes_Trabajadas\\LABELS\\0001_labels.png"
imagen = cv2.imread(ruta_imagen, cv2.IMREAD_GRAYSCALE)

fig, ax = plt.subplots()
ax.imshow(imagen, cmap="gray")
fig.canvas.mpl_connect("button_press_event", obtener_color)
plt.show()
