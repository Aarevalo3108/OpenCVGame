import cv2
import mediapipe as mp
import random
import time
import numpy as np

# Inicializar la cámara
cap = cv2.VideoCapture(0)

# Configurar MediaPipe para la detección de manos
mpHands = mp.solutions.hands
hands = mpHands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    min_detection_confidence=0.9,
    min_tracking_confidence=0.8
)
mpDraw = mp.solutions.drawing_utils

# Configuración inicial de la pelota
pelota_pos = (0, 0)
pelota_radio = 15
pelota_color = (0, 255, 0)  # Color de la pelota (verde)

# Función para generar obstáculos aleatorios con diferentes formas
def generar_obstaculos(num_obstaculos):
    obstaculos = []
    for _ in range(num_obstaculos):
        forma = random.choice(['rectangulo', 'triangulo', 'pentagono', 'rombo'])
        x = random.randint(100, 500)
        y = random.randint(100, 400)
        size = random.randint(50, 100)
        obstaculos.append((forma, x, y, size))
    return obstaculos

# Función para dibujar diferentes formas
def dibujar_forma(img, forma, x, y, size):
    if forma == 'rectangulo':
        cv2.rectangle(img, (x, y), (x + size, y + size), (0, 0, 255), 2)
    elif forma == 'triangulo':
        pts = np.array([[x, y], [x + size, y], [x + size // 2, y - size]], np.int32)
        pts = pts.reshape((-1, 1, 2))
        cv2.polylines(img, [pts], isClosed=True, color=(0, 0, 255), thickness=2)
    elif forma == 'pentagono':
        pts = np.array([[x + size // 2, y - size], [x + size, y - size // 3], [x + 3 * size // 4, y + size // 2],
                        [x + size // 4, y + size // 2], [x, y - size // 3]], np.int32)
        pts = pts.reshape((-1, 1, 2))
        cv2.polylines(img, [pts], isClosed=True, color=(0, 0, 255), thickness=2)
    elif forma == 'rombo':
        pts = np.array([[x + size // 2, y - size], [x + size, y], [x + size // 2, y + size], [x, y]], np.int32)
        pts = pts.reshape((-1, 1, 2))
        cv2.polylines(img, [pts], isClosed=True, color=(0, 0, 255), thickness=2)

# Generar obstáculos iniciales
num_obstaculos = 5
obstaculos = generar_obstaculos(num_obstaculos)

# Inicializar puntuación y tiempo
puntuacion = 0
inicio_tiempo = time.time()
ultimo_cambio_obstaculos = inicio_tiempo
ratio_puntuacion = 1  # Ratio de incremento de la puntuación

while True:
    success, img = cap.read()
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)
    
    # Verificar si se detectaron manos
    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            for id, lm in enumerate(handLms.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                
                # Si el punto de referencia es el ID 8 (punta del dedo índice)
                if id == 8:
                    pelota_pos = (cx, cy)

            # Dibujar las conexiones de la mano
            mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS)

    # Dibujar los obstáculos
    colision = False
    for (forma, x, y, size) in obstaculos:
        dibujar_forma(img, forma, x, y, size)
        
        # Comprobar colisión
        if (pelota_pos[0] + pelota_radio > x and
            pelota_pos[0] - pelota_radio < x + size and
            pelota_pos[1] + pelota_radio > y - size and
            pelota_pos[1] - pelota_radio < y + size):
            colision = True

    # Cambiar el color de la pelota si hay colisión
    if colision:
        pelota_color = (0, 0, 255)  # Rojo
        ratio_puntuacion = -0.5  # Reducir el ratio de puntuación
    else:
        pelota_color = (0, 255, 0)  # Verde
        ratio_puntuacion = 1  # Restaurar el ratio de puntuación

    # Calcular tiempo transcurrido
    tiempo_actual = time.time()
    tiempo_transcurrido = tiempo_actual - inicio_tiempo

    # Actualizar la puntuación
    puntuacion += ratio_puntuacion * (tiempo_actual - inicio_tiempo) * 0.01

    # Cambiar las posiciones de los obstáculos cada 5 segundos
    if tiempo_transcurrido - (ultimo_cambio_obstaculos - inicio_tiempo) >= 5:
        obstaculos = generar_obstaculos(num_obstaculos)
        ultimo_cambio_obstaculos = tiempo_actual

    # Dibujar la pelota
    cv2.circle(img, pelota_pos, pelota_radio, pelota_color, cv2.FILLED)

    # Mostrar la puntuación en la pantalla
    cv2.putText(img, f'Puntuacion: {int(puntuacion)}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)

    # Mostrar el tiempo en la pantalla
    cv2.putText(img, f'Tiempo: {int(tiempo_transcurrido)}s', (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)

    # Mostrar la imagen
    cv2.imshow("Image", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
