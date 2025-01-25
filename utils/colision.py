import numpy as np

# Función para comprobar colisión con diferentes formas
def comprobar_colision(pelota_pos, pelota_radio, forma, x, y, size):
    if forma == 'cuadrado':
        # Colisión con rectángulo
        return (pelota_pos[0] + pelota_radio > x and
                pelota_pos[0] - pelota_radio < x + size and
                pelota_pos[1] + pelota_radio > y and
                pelota_pos[1] - pelota_radio < y + size)
    elif forma == 'triangulo':
        # Colisión con triángulo (utilizando la función punto en triángulo)
        pts = np.array([[x, y], [x + size, y], [x + size // 2, y - size]], np.int32)
        return punto_en_triangulo(pelota_pos, pts)
    elif forma == 'pentagono':
        # Colisión con pentágono (utilizando la función punto en polígono)
        pts = np.array([[x + size // 2, y - size], [x + size, y - size // 3], [x + 3 * size // 4, y + size // 2],
                        [x + size // 4, y + size // 2], [x, y - size // 3]], np.int32)
        return punto_en_poligono(pelota_pos, pts)
    elif forma == 'rombo':
        # Colisión con rombo (utilizando la función punto en polígono)
        pts = np.array([[x + size // 2, y - size], [x + size, y], [x + size // 2, y + size], [x, y]], np.int32)
        return punto_en_poligono(pelota_pos, pts)
    return False

# Función para comprobar si un punto está dentro de un triángulo
def punto_en_triangulo(punto, tri):
    def signo(p1, p2, p3):
        return (p1[0] - p3[0]) * (p2[1] - p3[1]) - (p2[0] - p3[0]) * (p1[1] - p3[1])
    b1 = signo(punto, tri[0], tri[1]) < 0.0
    b2 = signo(punto, tri[1], tri[2]) < 0.0
    b3 = signo(punto, tri[2], tri[0]) < 0.0
    return ((b1 == b2) and (b2 == b3))

# Función para comprobar si un punto está dentro de un polígono
def punto_en_poligono(punto, poligono):
    n = len(poligono)
    dentro = False
    px, py = punto
    for i in range(n):
        j = (i + 1) % n
        xi, yi = poligono[i]
        xj, yj = poligono[j]
        if ((yi > py) != (yj > py)) and (px < (xj - xi) * (py - yi) / (yj - yi) + xi):
            dentro = not dentro
    return dentro