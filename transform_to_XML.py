import xml.etree.ElementTree as ET
from xml.dom import minidom


def create_xml_annotation(image_name, width, height, objects):
    # Crear el elemento raíz <annotation>
    root = ET.Element("annotation")

    # Añadir elementos necesarios
    folder = ET.SubElement(root, "folder").text = "nombre_de_la_carpeta"
    filename = ET.SubElement(root, "filename").text = image_name
    path = ET.SubElement(root, "path").text = "/ruta/completa/a/la/imagen/" + image_name
    source = ET.SubElement(root, "source")
    ET.SubElement(source, "database").text = "Desconocido"
    size = ET.SubElement(root, "size")
    ET.SubElement(size, "width").text = str(width)
    ET.SubElement(size, "height").text = str(height)
    ET.SubElement(size, "depth").text = "3"
    segmented = ET.SubElement(root, "segmented").text = "0"

    # Añadir objetos a la anotación
    for obj in objects:
        object_elem = ET.SubElement(root, "object")
        ET.SubElement(object_elem, "name").text = obj["label"]
        ET.SubElement(object_elem, "pose").text = "Desconocido"
        ET.SubElement(object_elem, "truncated").text = "0"
        ET.SubElement(object_elem, "difficult").text = "0"

        bndbox = ET.SubElement(object_elem, "bndbox")
        ET.SubElement(bndbox, "xmin").text = str(obj["xmin"])
        ET.SubElement(bndbox, "ymin").text = str(obj["ymin"])
        ET.SubElement(bndbox, "xmax").text = str(obj["xmax"])
        ET.SubElement(bndbox, "ymax").text = str(obj["ymax"])

    # Crear un objeto ElementTree para convertirlo a formato de cadena y guardar en un archivo XML
    tree = ET.ElementTree(root)
    with open("nombre_de_la_anotacion.xml", "wb") as file:
        tree.write(file)


# Ejemplo de uso
image_name = "nombre_de_la_imagen.png"
width = 800
height = 600
objects = [
    {"label": "objeto_1", "xmin": 10, "ymin": 20, "xmax": 100, "ymax": 150},
    {"label": "objeto_2", "xmin": 200, "ymin": 50, "xmax": 300, "ymax": 180},
    {"label": "objeto_3", "xmin": 350, "ymin": 100, "xmax": 500, "ymax": 250},
]

create_xml_annotation(image_name, width, height, objects)
