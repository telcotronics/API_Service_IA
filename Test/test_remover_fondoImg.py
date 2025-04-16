from rembg import remove
from PIL import Image
import numpy as np
import io

input_path = '/home/pablinux/Imágenes/S5/20170715_133343.jpg'
output_path = '/home/pablinux/Descargas/RESUL IA/imagen_sin_fondo.png'

# Abrir la imagen y eliminar el fondo
with open(input_path, 'rb') as i:
    input_data = i.read()
    output_data = remove(input_data)

# Guardar el resultado como PNG (para mantener la transparencia)
with open(output_path, 'wb') as o:
    o.write(output_data)

print("Fondo eliminado correctamente.")