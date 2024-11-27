import cv2
import mediapipe as mp

# Inicializar la cámara
cap = cv2.VideoCapture(0)

# Configurar MediaPipe para la detección de manos
mpHands = mp.solutions.hands
hands = mpHands.Hands(
    static_image_mode=False,
    max_num_hands=2,
    min_detection_confidence=0.9,
    min_tracking_confidence=0.8
)
mpDraw = mp.solutions.drawing_utils

# Configuración inicial de la pelota
pelota_pos = (0, 0)
pelota_radio = 25

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
                
                # Si el punto de referencia es el ID 8 (dedo indice), actualizar la posición de la pelota
                if id == 8:
                    pelota_pos = (cx, cy)

            # Dibujar las conexiones de la mano
            mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS)

    # Dibujar la pelota
    cv2.circle(img, pelota_pos, pelota_radio, (0, 255, 0), cv2.FILLED)

    # Mostrar la imagen
    cv2.imshow("Image", img)
    cv2.waitKey(1)
