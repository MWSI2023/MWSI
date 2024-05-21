import numpy as np
import cv2
from camaralib.digitalizar import digitalizar
from camaralib.guardar_img import guardar_img
from stokeslib.acoplar_mueller import acoplar_mueller

#Codigo de color
codigo=['R','G','B']

def guardar_mueller(M, path, name):

    #Mueller RGB
    M_RGB16 = np.zeros((M.shape[0]*3, M.shape[1]*3, 3), dtype = np.uint16)

    for i in range(3):
        #Acoplar en una imagen la Matriz de Mueller en el canal
        M_acoplada = acoplar_mueller(M[:,:,i,:,:])
        
        #Normalizar Mueller en 8 y 16 bits
        M_norm8 = digitalizar(M_acoplada, 'M8')
        M_RGB16[:,:,i] = digitalizar(M_acoplada, 'M16')

        #Colormap
        im = cv2.cvtColor(cv2.applyColorMap(M_norm8, cv2.COLORMAP_JET), cv2.COLOR_BGR2RGB)
            
        #Guardar
        guardar_img(path, im, name + '_' + codigo[i], cmap = 'jet', clim = [-1,1])
    
    #Guardar Mueller color
    cv2.imwrite(path + '/' + name + '.png', M_RGB16)

    return True

def guardar_mueller_canal(M, path, name):


    #Acoplar en una imagen la Matriz de Mueller en el canal
    M_acoplada = acoplar_mueller(M[:,:,:,:])
    
    #Normalizar Mueller en 8 y 16 bits
    M_norm8 = digitalizar(M_acoplada, 'M8')

    #Colormap
    im = cv2.cvtColor(cv2.applyColorMap(M_norm8, cv2.COLORMAP_JET), cv2.COLOR_BGR2RGB)
        
    #Guardar
    guardar_img(path, im, name, cmap = 'jet', clim = [-1,1])
  
    return True
