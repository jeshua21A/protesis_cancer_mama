import cv2
import imutils
import os
import numpy as np
import tkinter as tk
import vista_pantalla as vista
from PIL import Image as PILImage
from PIL import ImageTk

class ModeloPantalla:    
    def __init__ (self):
        self.pantalla = None
        self.camara = None
        self.frame = None
        
        self.rgb = 1
        self.gray = 0
        self.canny = 0

        self.slider_umbral_alto = None
        self.slider_umbral_bajo = None
        self.lblVideo = None        

    #Creamos el metodo visualizar para activar los fitros de la camara de video de nuestro dispositivo
    def visualizar(self):
        if self.camara is not None:
            validar, self.frame = self.camara.read()
            if validar == True:
                frame = self.frame
                if (self.rgb == 1):
                    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                elif (self.gray == 1):
                    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                elif (self.canny == 1):
                    grises = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

                    umbral_alto = self.slider_umbral_alto.get()
                    umbral_bajo = self.slider_umbral_bajo.get()

                    bordes_canny = cv2.Canny(grises, umbral_bajo, umbral_alto)

                    frame = cv2.bitwise_and(frame, frame, mask=bordes_canny)
                    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

                frame = imutils.resize(frame, width=620)

                #Manejo seguro de la imagen para mostrarla en pantalla
                if len(frame.shape) == 2:
                    imagen = PILImage.fromarray(frame).convert("RGB")
                else:
                    imagen = PILImage.fromarray(frame)

                imagen_a_video = ImageTk.PhotoImage(image=imagen)

                #Mostramos en la pantalla la camara de video
                self.lblVideo.configure(image=imagen_a_video)
                self.lblVideo.image = imagen_a_video
                self.lblVideo.after(10, self.visualizar)
            else:
                self.camara.release()

    #Creamos un metodo para activar la camara del disposiitivo
    def activar_camara(self):
        self.camara = cv2.VideoCapture(0)
        self.lblVideo = tk.Label(self.pantalla)
        self.lblVideo.place(x=345, y=60)
        self.visualizar()
        print("Camara seleccionada")

    #Creamos un metodo para deactivar la camara del dispositivo
    def desactivar_camara(self):
        self.camara.release()
        cv2.destroyAllWindows()
        self.lblVideo.destroy()
        print("Fin")

    #Creamos un metodo para cambiar la imagen de video a un filtro rgb
    def filtro_rgb(self):
        self.rgb = 1
        self.gray = 0
        self.canny = 0

    #Creamos un metodo para cambiar la imagen de video a un filtro en grises
    def filtro_gray(self):
        self.rgb = 0
        self.gray = 1
        self.canny = 0

    #Creamos un metodo para cambiar la imagen de video a un filtro de bordes
    def filtro_canny(self):
        self.rgb = 0
        self.gray = 0
        self.canny = 1