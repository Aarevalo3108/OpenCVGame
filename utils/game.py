import cv2
import mediapipe as mp
import time

from utils.obstacules import generar_obstaculos, dibujar_forma
from utils.colision import comprobar_colision


def init():
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
    # mpDraw = mp.solutions.drawing_utils

    # Configuración inicial de la pelota
    pelota_pos = (0, 0)
    pelota_radio = 15
    pelota_color = (0, 255, 0)  # Color de la pelota (verde)

    # Generar obstáculos iniciales
    num_obstaculos = 5
    obstaculos = generar_obstaculos(num_obstaculos)

    # Inicializar puntuación y tiempo
    puntuacion = 0
    inicio_tiempo = time.time()
    ultimo_cambio_obstaculos = inicio_tiempo
    ratio_puntuacion = 1  # Ratio de incremento de la puntuación

    # Inicializar variables
    vidas = 3  # Número de vidas
    tiempo_colision = None  # Variable para almacenar el tiempo de colisión

    while True:
        _, img = cap.read()
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = hands.process(imgRGB)
        
        # Verificar si se detectaron manos
        if results.multi_hand_landmarks:
            for handLms in results.multi_hand_landmarks:
                for id, lm in enumerate(handLms.landmark):
                    h, w, _ = img.shape
                    cx, cy = int(lm.x * w), int(lm.y * h)
                    
                    # Si el punto de referencia es el ID 8 (punta del dedo índice)
                    if id == 8:
                        pelota_pos = (cx, cy)

                # Dibujar las conexiones de la mano
                # mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS)

        # Dibujar los obstáculos
        colision = False
        for (forma, x, y, size) in obstaculos:
            dibujar_forma(img, forma, x, y, size)
            
            # Comprobar colisión
            if comprobar_colision(pelota_pos, pelota_radio, forma, x, y, size):
                colision = True
                if tiempo_colision is None:  # Inicializar el tiempo de colisión si no está ya en colisión
                    tiempo_colision = time.time()
                break

        # Si hay colisión y ha pasado más de un segundo en colisión, perder una vida
        if colision:
            if tiempo_colision is not None and time.time() - tiempo_colision >= 0.5:
                vidas -= 1
                tiempo_colision = time.time()  # Reiniciar el tiempo de colisión
                if vidas <= 0:
                    print("¡Juego terminado! Has perdido todas tus vidas.")
                    break
            pelota_color = (0, 0, 255)  # Rojo
            ratio_puntuacion = -0.5  # Reducir el ratio de puntuación
        else:
            pelota_color = (0, 255, 0)  # Verde
            ratio_puntuacion = 1  # Restaurar el ratio de puntuación
            tiempo_colision = None  # Reiniciar el tiempo de colisión si no hay colisión

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

        # Mostrar el número de vidas en la pantalla
        cv2.putText(img, f'Vidas: {vidas}', (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)

        # Mostrar la imagen
        cv2.imshow("Image", img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    print("Game Over")

