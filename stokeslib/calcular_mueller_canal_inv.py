import numpy as np

# Calcula matriz de Mueller en un canal (tiempo real)
# Recibe como entrada los vectores de stokes de entrada invertidos (Sin_inv) y los vectores de Stokes de salida (Sout)
# Devuelve la matriz de Mueller M del sistema en un único canal
#
# S_out_stat[:,:,:,:]:
#                       Primera componente: Dimensión vertical pixeles [0, dimy]
#                       Segunda componente: Dimensión horizonal pixeles [0, dimx]
#                       Tercer componente:  Dimensión horizonal pixeles (0,1,2)
#                       Cuarta componente:  Dimensión horizonal pixeles (B,G,R) (entradas)
#
# S_in_stat_inv[:,:,:,:]:
#                       Primera componente: Dimensión vertical pixeles [0, dimy]
#                       Segunda componente: Dimensión horizonal pixeles [0, dimx]
#                       Tercer componente:  
#                       Cuarta componente:  
#
# M[:,:,:,:]: 
#               Primera componente: Dimensión vertical pixeles [0, dimy]
#               Segunda componente: Dimensión horizonal pixeles [0, dimx]
#                Cuarta componente: Dimensión vertical de la matriz (0,1,2)
#                Quinta componente: Dimensión horizontal de la matriz (0,1,2)

def calcular_mueller_canal_inv(S_in_stat_inv,S_out_stat):
  Mueller_img = np.einsum('ijlm,ijmn->ijln',S_out_stat,S_in_stat_inv)
  return Mueller_img
