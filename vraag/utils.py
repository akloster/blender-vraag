import numpy as np

def vector(*v):
    a = np.array(v, dtype=np.float)
    a.shape = (len(v),1)
    return a


identity = lambda: np.identity(4, dtype=np.float)

up = vector(0,0,1) 
right = vector(1,0,0)
left = vector(-1,0,0)
down = vector(0,0,-1)
front = vector(0,-1,0)
back = vector(0,1,0)
