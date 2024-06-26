import sys
import os
import numpy as np
from threading import Thread
from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow, QGraphicsScene, QGraphicsView
from PyQt5.uic import loadUi
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import QLibraryInfo
from simple_pyspin import Camera
import cv2

sys.path.append('../')
from stokeslib.polarization_full_dec_array import polarization_full_dec_array
from stokeslib.calcular_stokes import calcular_stokes
from stokeslib.calcular_mueller_canal_inv import calcular_mueller_canal_inv 
from stokeslib.acoplar_mueller import acoplar_mueller 
from stokeslib.mueller_mean import mueller_mean
from stokeslib.normalizar_mueller import normalizar_mueller
from camaralib.digitalizar import digitalizar
from raspberrylib.runcmd import runcmd
from stokeslib.calcular_propiedades import calcular_dolp, calcular_aolp
from camaralib.guardar_mueller import guardar_mueller_canal

os.environ["QT_QPA_PLATFORM_PLUGIN_PATH"] = QLibraryInfo.location(
    QLibraryInfo.PluginsPath
)

#Threading motores
class thread_motor(Thread):
    def __init__(self, motor, movimiento):
        super(thread_motor, self).__init__()
        self.motor = motor
        self.movimiento = movimiento
    def run(self):
        comando = "cd raspberrylib/; python3 motor_control_ssh.py " + self.motor + ' ' + self.movimiento
        runcmd(comando, verbose=True)

# Configuración inicial cámara
exposure_time = 5000
interpolador = 'vecinos'
N = 1

#Decimador imagen
decimador = 2

class Ui(QMainWindow):
    def __init__(self, cam):
        super(Ui, self).__init__()

        #Objeto cámara
        self.cam = cam

        # Carga GUI diseñado
        loadUi('gui/gui.ui', self)      
            
        #Inicializa Cámara
        self.start_cam(self)

        #Configura Cámara
        self.config_cam(self)

        #Muestra imagen
        self.start_recording(self) 

        #Espera boton motor
        self.motor_listen(self)

        #Espera boton captura
        self.capture_listen(self)

        #Espera cambios en la configuración
        self.config_listen(self)

        #Muestra GUI
        self.show()

    def start_cam(self, label):

        #Modo de Exposición
        self.cam.ExposureAuto = 'Off'
    	
        #Tiempo de exposición
        self.exposure_time = exposure_time

        #Número de promedios
        self.N = N

        #Formato
        self.cam.PixelFormat = "BayerRG8"

        #Inicia cámara
        self.cam.start()

    def config_cam(self, label):
        #Cambia tiempo de exposición
        self.cam.ExposureTime = self.exposure_time

    def config_program(self, label):
        #Cambia número de promedio
        self.N = self.new_N

    def start_recording(self, label):  
        #Timer 	
        timer = QtCore.QTimer(self)
        
        #Conexión
        timer.timeout.connect(self.update_image)
        timer.start(0)
        self.update_image()    

    def update_image(self):
        #Actualiza configuración
        self.interpolador = 'vecinos' if self.vecinos_btn.isChecked() else 'bilineal'
        self.exposure_time = int(self.exposicion_edit.text())
        self.new_N = int(self.N_edit.text())

        #Captura imagen
        raws = [np.uint16(self.cam.get_array()) for n in range(self.N)]
        raw = (1/self.N*sum(raws)).astype(np.uint8)
        
        #Medibles
        I90, I45, I135, I0 = polarization_full_dec_array(raw, interpolacion = self.interpolador)

        #Stokes
        S0, S1, S2 = calcular_stokes(I90, I45, I135, I0)

        #Medida a mostrar
        medida_str = self.medida_box.currentText()

        if medida_str == 'DoLP':
            medida = digitalizar(calcular_dolp(S0, S1, S2), 'DoLP')
        elif medida_str == 'AoLP':
            medida = digitalizar(calcular_aolp(S1, S2), 'AoLP')
        else:
            medida = digitalizar(locals()[medida_str], medida_str)
        
        #Imagen de la medida elegida
        img = (medida[::decimador,::decimador,:]).astype(np.uint8)
        img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        
        #Formato Array to PixMap
        h, w, _ = img.shape
        S0QIMG = QImage(img, w, h, QImage.Format_RGB888)
        pixmap = QPixmap(S0QIMG)

        #Plot
        self.img.setPixmap(pixmap)

    def move_up(self):
        thread = thread_motor("Y","B")
        thread.start()

    def move_down(self):
        thread = thread_motor("Y","F")
        thread.start()

    def move_left(self):
        thread = thread_motor("X","B")
        thread.start()

    def move_right(self):
        thread = thread_motor("X","F")
        thread.start()  

    def rotate_left(self):
        thread = thread_motor("T","B")
        thread.start()  

    def rotate_right(self):
        thread = thread_motor("T","F")
        thread.start()  

    def auto_capture(self):
        self.cam.stop()
        runcmd("cd ../; python3 simple_mueller.py", verbose=True)
        self.cam.start()
   
    def motor_listen(self, label):
        #Arriba
        up_btn = self.up_btn
        up_btn.clicked.connect(self.move_up)
        
        #Abajo
        dwn_btn = self.dwn_btn
        dwn_btn.clicked.connect(self.move_down)
        
        #Izquierda
        left_btn = self.left_btn
        left_btn.clicked.connect(self.move_left)
        
        #Derecha
        right_btn = self.right_btn
        right_btn.clicked.connect(self.move_right)

        #Girar izquierda
        rotate_left_btn = self.rotate_left_btn
        rotate_left_btn.clicked.connect(self.rotate_left)

        #Girar derecha
        rotate_right_btn = self.rotate_right_btn
        rotate_right_btn.clicked.connect(self.rotate_right)
    
    def capture_listen(self, label):
        capture_btn = self.capture_btn
        capture_btn.clicked.connect(self.auto_capture)

    def config_listen(self, label):
        config_btn = self.config_btn
        #Camara
        config_btn.clicked.connect(self.config_cam)
        #Programa
        config_btn.clicked.connect(self.config_program)

def main(cam):
    app = QApplication(sys.argv)
    instance = Ui(cam)
    app.exec_()

if __name__ == "__main__":

    #Inicia GUI
    with Camera() as cam:
        main(cam)      
    
    #Detener cámara
    cam.stop()  

    #Salir
    sys.exit()
