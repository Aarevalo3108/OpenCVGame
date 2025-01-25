import cv2
import numpy as np
import random

# Función para generar obstáculos aleatorios con diferentes formas
def generar_obstaculos(num_obstaculos):
    obstaculos = []
    for _ in range(num_obstaculos):
        forma = random.choice(['cuadrado', 'triangulo', 'pentagono', 'rombo'])
        x = random.randint(100, 500)
        y = random.randint(100, 400)
        size = random.randint(50, 100)
        obstaculos.append((forma, x, y, size))
    return obstaculos

# Función para dibujar diferentes formas
def dibujar_forma(img, forma, x, y, size):
    if forma == 'cuadrado':
        cv2.rectangle(img, (x, y), (x + size, y + size), (0, 255, 0), 2)
    elif forma == 'triangulo':
        pts = np.array([[x, y], [x + size, y], [x + size // 2, y - size]], np.int32)
        pts = pts.reshape((-1, 1, 2))
        cv2.polylines(img, [pts], isClosed=True, color=(0, 0, 255), thickness=2)
    elif forma == 'pentagono':
        pts = np.array([[x + size // 2, y - size], [x + size, y - size // 3], [x + 3 * size // 4, y + size // 2],
                        [x + size // 4, y + size // 2], [x, y - size // 3]], np.int32)
        pts = pts.reshape((-1, 1, 2))
        cv2.polylines(img, [pts], isClosed=True, color=(255, 0, 0), thickness=2)
    elif forma == 'rombo':
        pts = np.array([[x + size // 2, y - size], [x + size, y], [x + size // 2, y + size], [x, y]], np.int32)
        pts = pts.reshape((-1, 1, 2))
        cv2.polylines(img, [pts], isClosed=True, color=(125, 125, 0), thickness=2)