from ultralytics import YOLO

def main():
    # Entrenar
    model = YOLO('yolo11n.pt')

    model.train(
        # Cargar modelo base YOLOv11
        data='C:/Users/jeshu/Documents/Python/Proyecto_Cancer_Mama/Detector_Objetos_Yolov11/Dataset_Yolov11/data.yaml',
        epochs=50,               # número de épocas
        imgsz=640,               # tamaño de imagen
        batch=8,                 # tamaño de lote
        device=0,                # GPU (0)
        workers=0,
        half=False
    )

if __name__ == "__main__":
    main()
