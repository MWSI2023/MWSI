import numpy as np

#Desacoplar imagen y recuperar array en RGB

def desacoplar_mueller(M_show):
  M = np.zeros((M_show.shape[0]//3,M_show.shape[1]//3,3,3,3),dtype=float)
  for i in range(3):
    for j in range(3):
      for k in range(3):
        M[:,:,k,i,j] = M_show[i*1024:(i+1)*1024,j*1224:(j+1)*1224,k]
  return M
