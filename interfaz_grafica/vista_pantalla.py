#Importación de librerias
from tkinter import *
from PIL import Image, ImageTk
import cv2
import imutils
import numpy as np
import os

#Creamos el metodo visualizar para activar los fitros de la camara de video de nuestro dispositivo
def visualizar():
    global pantalla, frame, rgb, gray, canny, slider_umbral_alto, slider_umbral_bajo

    if camara is not None:
        validar, frame = camara.read()

        if validar == True:

            if (rgb == 1 and gray == 0):
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            elif (rgb == 0 and gray == 1):
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            elif (canny == 1):
                grises = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

                umbral_alto = slider_umbral_alto.get()
                umbral_bajo = slider_umbral_bajo.get()

                bordes_canny = cv2.Canny(grises, umbral_bajo, umbral_alto)

                frame = cv2.bitwise_and(frame, frame, mask=bordes_canny)

            frame = imutils.resize(frame, width=620)

            imagen_video = Image.fromarray(frame)
            convertir_imagen_video = ImageTk.PhotoImage(image=imagen_video)

            #Mostramos en la pantalla la camara de video
            lblVideo.configure(image=convertir_imagen_video)
            lblVideo.image = convertir_imagen_video
            lblVideo.after(10, visualizar)
        
        else:
            camara.release()

#Creamos un metodo para activar la camara del disposiitivo
def activar_camara():
    global camara, lblVideo
    camara = cv2.VideoCapture(0)
    lblVideo = Label(pantalla)
    lblVideo.place(x=345, y=60)
    visualizar()
    print("Camara seleccionada")

#Creamos un metodo para deactivar la camara del dispositivo
def desactivar_camara():
    camara.release()
    cv2.destroyAllWindows()
    lblVideo.destroy()
    print("Fin")

#Creamos un metodo para cambiar la imagen de video a un filtro rgb
def filtro_rgb():
    global rgb, gray, canny
    rgb = 1
    gray = 0
    canny = 0

#Creamos un metodo para cambiar la imagen de video a un filtro en grises
def filtro_gray():
    global rgb, gray, canny
    rgb = 0
    gray = 1
    canny = 0

#Creamos un metodo para cambiar la imagen de video a un filtro de bordes
def filtro_canny():
    global rgb, gray, canny
    rgb = 0
    gray = 0
    canny = 1

#Creamos un metodo para guardas las capturas de pantalla con los filtros aplicados
def captura_video():
    global frame
    archivos_imagenes_captura = os.listdir('Imagenes de captura')
    numero_archivos = len(archivos_imagenes_captura)-1
    print("Numero de archivos de la carpeta Imagenes de captura: "+str(numero_archivos))
    indice = numero_archivos + 1
    if (rgb == 1):
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        cv2.imwrite('Imagenes de captura/Imagen_Modelo_No_'+str(indice)+'.jpg', frame)
    else:
        cv2.imwrite('Imagenes de captura/Imagen_Modelo_No_'+str(indice)+'.jpg', frame)

#Variables necesarias para hacer funcionar nuestros metodos
camara = None
rgb = 1
gray = 0
canny = 0

#Construcción de la pantalla
pantalla = Tk()
pantalla.title("Escaner Modelador")
pantalla.geometry("1038x650")
pantalla.resizable(0,0)

#Implementar una imagen de fondo para personalizar la pantalla
ruta_imagen_fondo = "Detalles de pantalla/fondo_de_pantalla.png"
imagen_fondo = PhotoImage(file=ruta_imagen_fondo)
background = Label(image=imagen_fondo, text="Fondo")
background.place(x=0, y=0, relwidth=1, relheight=1)

#Implementar etiquetas de texto en la pantalla
etiqueta_control = Label(pantalla, text="CONTROLES DE VIDEO:")
etiqueta_control.place(x=100, y=10)

etiqueta_video = Label(pantalla, text="VIDEO EN TIEMPO REAL:")
etiqueta_video.place(x=580, y=10)

etiqueta_filtro = Label(pantalla, text="FILTROS DE CAMARA:")
etiqueta_filtro.place(x=104, y=220)

etiqueta_canny = Label(pantalla, text="CONTROL DE UMBRALES DE CANNY:")
etiqueta_canny.place(x=57, y=436)

#Construcción de los botones para navegar con las funciones d ela pantalla
ruta_imagen_boton_inicio = "Detalles de pantalla/abierto.png"
imagen_boton_inicio = PhotoImage(file=ruta_imagen_boton_inicio)
boton_inicio = Button(pantalla, text="Iniciar", image=imagen_boton_inicio, width=90, height=60, font=("Calibri", 12), command=activar_camara)
boton_inicio.place(x=70, y=60)

ruta_imagen_boton_fin = "Detalles de pantalla/cerrar.png"
imagen_boton_fin= PhotoImage(file=ruta_imagen_boton_fin)
boton_fin = Button(pantalla, text="Terminar", image=imagen_boton_fin, width=90, height=60, font=("Calibri", 12), command=desactivar_camara)
boton_fin.place(x=180, y=60)

ruta_imagen_boton_captura = "Detalles de pantalla/captura.png"
imagen_boton_captura= PhotoImage(file=ruta_imagen_boton_captura)
boton_captura = Button(pantalla, text="Capturar", image=imagen_boton_captura, width=200, height=50, font=("Calibri", 12), command=captura_video)
boton_captura.place(x=70, y=137)

ruta_imagen_boton_rgb = "Detalles de pantalla/rgb.png"
imagen_boton_rgb= PhotoImage(file=ruta_imagen_boton_rgb)
boton_rgb = Button(pantalla, text="RGB", image=imagen_boton_rgb, width=200, height=40, font=("Calibri", 12), command=filtro_rgb)
boton_rgb.place(x=70, y=265)

ruta_imagen_boton_grises = "Detalles de pantalla/grises.png"
imagen_boton_grise= PhotoImage(file=ruta_imagen_boton_grises)
boton_grises = Button(pantalla, text="Grises", image=imagen_boton_grise, width=200, height=40, font=("Calibri", 12), command=filtro_gray)
boton_grises.place(x=70, y=315)

ruta_imagen_boton_canny = "Detalles de pantalla/canny.png"
imagen_boton_canny = PhotoImage(file=ruta_imagen_boton_canny)
boton_canny = Button(pantalla, text="Canny", image=imagen_boton_canny, width=200, height=40, font=("Calibri", 12), command=filtro_canny)
boton_canny.place(x=70, y=365)

#Sliders para controlar el valor de los umbrales alto y bajo del filtro de cámara: "Canny"
slider_umbral_alto = Scale(pantalla, from_=0, to=255, orient=HORIZONTAL)
slider_umbral_alto.place(x=70, y=490, width=205)

slider_umbral_bajo = Scale(pantalla, from_=0, to=255, orient=HORIZONTAL)
slider_umbral_bajo.place(x=70, y=560, width=205)

#Ubicacion de la camara de video
lblVideo = Label(pantalla)

#Proyección de la pantalla
pantalla.mainloop()