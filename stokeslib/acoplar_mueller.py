import numpy as np

def acoplar_mueller(M):

  M_show = M.copy()
  M1_show = np.append(M_show[:,:,0,0], M_show[:,:,0,1], axis=1)
  M1_show = np.append(M1_show, M_show[:,:,0,2], axis=1)
  M2_show = np.append(M_show[:,:,1,0], M_show[:,:,1,1], axis=1)
  M2_show = np.append(M2_show, M_show[:,:,1,2], axis=1)
  M3_show = np.append(M_show[:,:,2,0], M_show[:,:,2,1], axis=1)
  M3_show = np.append(M3_show, M_show[:,:,2,2], axis=1)
  M_show = np.append(M1_show, M2_show, axis = 0)
  M_show = np.append(M_show, M3_show, axis = 0)
  
  return M_show
