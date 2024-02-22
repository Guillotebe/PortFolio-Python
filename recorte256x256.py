# Nombre del archivo: recorte256x256.py
# Autor: Guillermo Bellone
# Fecha de creación: 20 de Diciembre de 2023
# Descripción: recorta una imagen a una tamaño de 256x256 dejando seleccionar area.
# version: 1.0.0


from PIL import Image, ImageTk
import tkinter as tk
from tkinter import filedialog


class AplicacionRecorteImagen:
    def __init__(self, root):
        self.root = root
        self.root.title("Recortar Imagen")

        self.canvas = tk.Canvas(root)
        self.canvas.pack(expand=tk.YES, fill=tk.BOTH)

        self.boton_seleccionar = tk.Button(
            root, text="Seleccionar Imagen", command=self.seleccionar_imagen
        )
        self.boton_seleccionar.pack(pady=10)

        self.boton_recortar = tk.Button(
            root, text="Recortar", command=self.recortar_imagen
        )
        self.boton_recortar.pack(pady=5)

        self.ruta_imagen = None
        self.imagen = None
        self.imagen_tk = None
        self.caja_recorte = None

    def seleccionar_imagen(self):
        self.ruta_imagen = filedialog.askopenfilename(
            title="Seleccionar imagen",
            filetypes=[("Archivos de imagen", "*.png;*.jpg;*.jpeg")],
        )

        if self.ruta_imagen:
            self.imagen = Image.open(self.ruta_imagen)
            self.imagen_tk = ImageTk.PhotoImage(self.imagen)
            self.canvas.config(width=self.imagen.width, height=self.imagen.height)
            self.canvas.create_image(0, 0, anchor=tk.NW, image=self.imagen_tk)

            # Crear una caja de selección inicial
            self.caja_recorte = self.canvas.create_rectangle(
                0, 0, 256, 256, outline="red"
            )

            self.canvas.bind("<B1-Motion>", self.actualizar_caja_recorte)

    def actualizar_caja_recorte(self, event):
        x, y = event.x, event.y
        self.canvas.coords(self.caja_recorte, x, y, x + 256, y + 256)

    def recortar_imagen(self):
        if self.ruta_imagen:
            x1, y1, x2, y2 = self.canvas.coords(self.caja_recorte)
            x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)

            # Recortar la región seleccionada
            imagen_recortada = self.imagen.crop((x1, y1, x2, y2))

            # Guardar la imagen recortada en la ruta específica
            ruta_salida = "c:\\Users\\User\\Desktop\\imagen_recortada.png"
            imagen_recortada.save(ruta_salida)

            print("Imagen recortada y guardada correctamente en", ruta_salida)


if __name__ == "__main__":
    root = tk.Tk()
    app = AplicacionRecorteImagen(root)
    root.mainloop()
