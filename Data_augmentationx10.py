import os
import cv2

contador = 511
# Ruta de la carpeta que contiene las imágenes originales
input_folder = "c:\\Users\\User\\Desktop\\DIGPATHO\\IMAGENES\\Crudo para segundo entrenamiento ki67\\Imagenes_Trabajadas\\RESULTADOS\\originales"

# Ruta de la carpeta donde se guardarán las imágenes aumentadas
output_folder = "c:\\Users\\User\\Desktop\\DIGPATHO\\IMAGENES\\Crudo para segundo entrenamiento ki67\\Imagenes_Trabajadas\\Data augmentation\\org"

# Asegúrate de que la carpeta de salida exista, si no, créala
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Lista de transformaciones que deseas aplicar
transformations = [
    ("rotate", 45),  # Rotar la imagen 45 grados
    ("rotate", -45),  # Rotar la imagen -45 grados
    ("rotate", 90),  # Rotar la imagen 90 grados
    ("rotate", -90),  # Rotar la imagen -90 grados
    ("rotate", 180),  # Rotar la imagen 180 grados
    ("flip_horizontal", None),  # Voltear horizontalmente
    ("flip_vertical", None),  # Voltear verticalmente
    ("translate", (10, 20)),  # Desplazar la imagen en dirección x:10, y:20 píxeles
    ("translate", (-15, 5)),  # Desplazar la imagen en dirección x:-15, y:5 píxeles
    ("shear", 0.2),  # Deformación (shear) de la imagen
    ("shear", -0.2),  # Otra deformación (shear) en dirección opuesta
]

# Itera sobre cada imagen en la carpeta de entrada
for filename in os.listdir(input_folder):
    if filename.endswith(".jpg") or filename.endswith(".png"):
        # Asegúrate de que solo procese archivos de imagen
        image_path = os.path.join(input_folder, filename)

        # Lee la imagen usando OpenCV
        img = cv2.imread(image_path)

        # Itera sobre cada transformación y aplica de manera acumulativa
        for operation, param in transformations:
            contador += 1
            img_transformed = img.copy()  # Crea una copia de la imagen original

            if operation == "rotate":
                matrix = cv2.getRotationMatrix2D(
                    (img.shape[1] / 2, img.shape[0] / 2), param, 1
                )
                # Configura el modo de borde para replicar valores de píxeles
                img_transformed = cv2.warpAffine(
                    img_transformed,
                    matrix,
                    (img_transformed.shape[1], img_transformed.shape[0]),
                    borderMode=cv2.BORDER_CONSTANT,
                    borderValue=(1, 1, 1),
                )
            elif operation == "flip_horizontal":
                img_transformed = cv2.flip(img_transformed, 1)
            elif operation == "flip_vertical":
                img_transformed = cv2.flip(img_transformed, 0)
            elif operation == "blur":
                img_transformed = cv2.GaussianBlur(img_transformed, (param, param), 0)
            elif operation == "scale":
                img_transformed = cv2.resize(img_transformed, None, fx=param, fy=param)

            # Guarda la imagen aumentada en la carpeta de salida
            output_path = os.path.join(output_folder, f"org_{contador}.png")
            cv2.imwrite(output_path, img_transformed)

print("Transformaciones aplicadas con éxito.")
