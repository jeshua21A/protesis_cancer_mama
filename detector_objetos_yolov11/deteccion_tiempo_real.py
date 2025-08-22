import cv2
from ultralytics import YOLO

# Cargar modelo entrenado (YOLOv11)
model = YOLO('runs/detect/train22/weights/best.pt')

# Abrir cámara (0 = cámara por defecto)
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Predecir objetos en el frame
    results = model(frame)

    # Dibujar cajas y etiquetas en el frame
    annotated_frame = results[0].plot()  # genera la imagen con los cuadros

    # Mostrar la imagen
    cv2.imshow('Detección en tiempo real', annotated_frame)

    # Salir al presionar 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Liberar la cámara y cerrar ventanas
cap.release()
cv2.destroyAllWindows()