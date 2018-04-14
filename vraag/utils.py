import numpy as np
import math

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
forward = back
backwards = front
def rotation_matrix(axis, angle):
    """ generate rotation matrix from axis/angle.
        Code taken from Stack Overflow
    """

    theta = angle/360*math.pi
    axis = np.array(axis, dtype=np.float)
    axis /= np.linalg.norm(axis)
    a = math.cos(theta)
    b, c, d = -axis*math.sin(theta)
    aa, bb, cc, dd = a*a, b*b, c*c, d*d
    bc, ad, ac, ab, bd, cd = b*c, a*d, a*c, a*b, b*d, c*d
    return np.array([[aa+bb-cc-dd, 2*(bc+ad), 2*(bd-ac),0],
                     [2*(bc-ad), aa+cc-bb-dd, 2*(cd+ab),0],
                     [2*(bd+ac), 2*(cd-ab), aa+dd-bb-cc,0],
                     [0,0,0,1]], dtype=np.float)

