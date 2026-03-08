import cv2
import imutils
import os
import numpy as np
import modelo_pantalla as modelo
import vista_pantalla as vista
import tkinter as tk
from PIL import Image, ImageTk

class ControladorPantalla:
    def __init__ (self, modelo, vista):
        self.modelo = modelo
        self.vista = vista

        self.modelo.pantalla = self.vista.pantalla 
        self.modelo.slider_umbral_alto = self.vista.slider_umbral_alto
        self.modelo.slider_umbral_bajo = self.vista.slider_umbral_bajo
        self.modelo.lblVideo = self.vista.lblVideo

        self.vista.boton_inicio.config(command=self.activar_camara)
        self.vista.boton_fin.config(command=self.desactivar_camara)
        self.vista.boton_captura.config(command=self.captura_video)
        self.vista.boton_rgb.config(command=self.filtro_rgb)
        self.vista.boton_grises.config(command=self.filtro_gray)
        self.vista.boton_canny.config(command=self.filtro_canny)

    # Eventos de los botones
    def activar_camara(self):
        self.modelo.activar_camara()

    def desactivar_camara(self):
        self.modelo.desactivar_camara()

    def captura_video(self):
        self.modelo.captura_video()
    
    def filtro_rgb(self):
        self.modelo.filtro_rgb()
    
    def filtro_gray(self):
        self.modelo.filtro_gray()

    def filtro_canny(self):
        self.modelo.filtro_canny()