# PARA LOS PEQUEÑOS ERRORES QUE HAYA DEBERÍA APLICAR [Levenshtein distance] https://en.wikipedia.org/wiki/Levenshtein_distance#:~:text=Informally%2C%20the%20Levenshtein%20distance%20between,considered%20this%20distance%20in%201965.
# AUNQUE MEJOR APLICAR [Damerau-Levenshtein] https://en.wikipedia.org/wiki/Damerau%E2%80%93Levenshtein_distance
# Falta mejorar el codigo 
import cv2
from matplotlib import pyplot as plt
import numpy as np

images_to_process = []

for row in range(4):
    for column in range(6):
        #img = cv2.imread(f"img/imagenesAescanear/img_sin_procesar{row}{column}.jpg")
        img = cv2.imread(f"C:/Users/Alex/Desktop/Discord Snipe Warframe/PROYECTO INVENTARIO OCR/img/imagenesAescanear/img_sin_procesar{row}{column}.jpg")
        images_to_process.append(img)

def grayscale(image):
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

def noise_removal(image):
    import numpy as np
    kernel = np.ones((1, 1), np.uint8)
    image = cv2.dilate(image, kernel, iterations=1)
    kernel = np.ones((1, 1), np.uint8)
    image = cv2.erode(image, kernel, iterations=1)
    image = cv2.morphologyEx(image, cv2.MORPH_CLOSE, kernel)
    image = cv2.medianBlur(image, 3)
    return (image)

def thin_font(image):
    import numpy as np
    image = cv2.bitwise_not(image)
    kernel = np.ones((2,2),np.uint8)
    image = cv2.erode(image, kernel, iterations=1)
    image = cv2.bitwise_not(image)
    return (image)

def thick_font(image):
    import numpy as np
    image = cv2.bitwise_not(image)
    kernel = np.ones((2,2),np.uint8)
    image = cv2.dilate(image, kernel, iterations=1)
    image = cv2.bitwise_not(image)
    return (image)

from PIL import Image

processed_images = []

for img in images_to_process:
    inverted_image = cv2.bitwise_not(img)
    thresh, im_bw2 = cv2.threshold(inverted_image, 0, 255, cv2.THRESH_BINARY)
    eroded_image = thick_font(im_bw2)
    inverted_image = cv2.bitwise_not(im_bw2)
    gray_image2 = grayscale(inverted_image)
    inverted_image = cv2.bitwise_not(gray_image2)
    eroded_image = thick_font(inverted_image)
    eroded_image = thick_font(eroded_image)

    thresh, im_bw2 = cv2.threshold(eroded_image, 250, 255, cv2.THRESH_BINARY)
    eroded_image = thin_font(eroded_image)
    thresh, im_bw2 = cv2.threshold(eroded_image, 240, 255, cv2.THRESH_BINARY)
    processed_images.append(im_bw2)

for index, x in enumerate(processed_images):
        cv2.imwrite(f"img/imagenesAescanear/img_procesada_{index}.jpg", processed_images[index])

class Items:
  def __init__(self, cantidad, nombre):
   self.nombre = nombre
   self.cantidad = cantidad

items = []
print("--------------EASYOCR-----------")
import easyocr
reader = easyocr.Reader(['en'],gpu=False)
for i, img in enumerate(processed_images):
    result = reader.readtext(img, detail=0)
    items.insert(i,Items(result[0],' '.join([str(x) for x in result[1:len(result)]]).replace("Blueprint","").strip()))
    print(result)

# TODO: Aplicar algoritmo Damerau-Levenshtein python
def damerau_levenshtein_distance(s1, s2):
    d = {}
    lenstr1 = len(s1)
    lenstr2 = len(s2)
    for i in range(-1,lenstr1+1):
        d[(i,-1)] = i+1
    for j in range(-1,lenstr2+1):
        d[(-1,j)] = j+1

    for i in range(lenstr1):
        for j in range(lenstr2):
            if s1[i] == s2[j]:
                cost = 0
            else:
                cost = 1
            d[(i,j)] = min(
                           d[(i-1,j)] + 1, # deletion
                           d[(i,j-1)] + 1, # insertion
                           d[(i-1,j-1)] + cost, # substitution
                          )
            if i and j and s1[i]==s2[j-1] and s1[i-1] == s2[j]:
                d[(i,j)] = min (d[(i,j)], d[i-2,j-2] + cost) # transposition

    return d[lenstr1-1,lenstr2-1]

from os import path
lines = []
path = ""
with open(path.expandvars(path),encoding="utf8") as f:
    lines = f.readlines()
    

for i, item in enumerate(items):
    distancia_menor_linea = 10
    menor_linea = 0 
    for line in lines:
        line = line.rstrip()
        distancia = damerau_levenshtein_distance(item.nombre,line)
        if(distancia < distancia_menor_linea):
            menor_linea = lines.index(line+"\n")
            distancia_menor_linea = distancia
    items[i].nombre = lines[menor_linea].rstrip()
#Datos a CSV
import csv
filename = 'inventario.csv'
modo = "a+"
try:
    with open(filename, modo,encoding='UTF8', newline='') as f:
        writer = csv.writer(f, delimiter=";")
        writer.writerow(['Item','Cantidad'])
        for item in items:
            writer.writerow([item.nombre,item.cantidad])
except BaseException as e:
    print('BaseException:', e)
else:
    print('Data has been loaded successfully !')

