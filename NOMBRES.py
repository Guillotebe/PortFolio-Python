import os


def cambiar_nombres(carpeta_origen_labels, carpeta_origen_originales, inicio):
    # Listar archivos en las carpetas de origen
    archivos_labels = sorted(os.listdir(carpeta_origen_labels))
    archivos_originales = sorted(os.listdir(carpeta_origen_originales))

    # Función para cambiar el nombre de los archivos en una carpeta específica
    def renombrar_carpeta(origen, carpeta, prefijo):
        print(f"La carpeta seleccionada es: {origen}")
        for i, archivo in enumerate(origen):
            ruta_archivo = os.path.join(carpeta, archivo)
            nuevo_nombre = f"{prefijo}_{inicio + i}.png"
            nueva_ruta_archivo = os.path.join(carpeta, nuevo_nombre)
            os.rename(ruta_archivo, nueva_ruta_archivo)
            print(f"Renombrado: {archivo} -> {nuevo_nombre}")

    # Llamar a la función para cambiar nombres en ambas carpetas
    renombrar_carpeta(archivos_labels, carpeta_labels, "lbl")
    renombrar_carpeta(archivos_originales, carpeta_originales, "org")


if __name__ == "__main__":
    # Especifica las carpetas de origen
    carpeta_labels = "c:\\Users\\User\\Desktop\\DIGPATHO\\IMAGENES\\Crudo para segundo entrenamiento ki67\\Imagenes_Trabajadas\\RESHAPE\\resultado_65\\labels"
    carpeta_originales = "c:\\Users\\User\\Desktop\\DIGPATHO\\IMAGENES\\Crudo para segundo entrenamiento ki67\\Imagenes_Trabajadas\\RESHAPE\\resultado_65\\originales"

    # Especifica el número de inicio
    inicio = 512  # Puedes ajustar el número de inicio según la ultima imagen cargada (si es 215 la ultima. Colocas 216)

    # Llama a la función para cambiar los nombres de los archivos
    cambiar_nombres(carpeta_labels, carpeta_originales, inicio)

# IMAGENES/Crudo para segundo entrenamiento ki67/Imagenes_Trabajadas/RESHAPE
