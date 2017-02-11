import numpy as np
import math
import bpy
from vraag.utils import *

from .base import VraagConstruct, register_constructor

class VraagTransformation(VraagConstruct):
    def __init__(self, parent):
        super().__init__(parent)
        self.matrix = identity()
        

class Translate(VraagTransformation):
    def __init__(self, parent, v):
        super().__init__(parent)
        v = np.array(v, dtype=np.float)
        self.v = v
        self.matrix[3,0:3] = v.transpose()


register_constructor(Translate, "translate")

class Scale(VraagTransformation):
    def __init__(self, parent, *args):
        super().__init__(parent)
        if len(args)==1:
            scaler=[args]
            try:
                if len(args[0]):
                    scaler = args[0]
            except TypeError:
                if len(args):
                    scaler = args
        else:
            scaler = args
        if len(scaler)==1:
            self.matrix[0,0] = scaler[0]
            self.matrix[1,1] = scaler[0]
            self.matrix[2,2] = scaler[0]
        else:
            self.matrix[0,0] = scaler[0]
            self.matrix[1,1] = scaler[1]
            self.matrix[2,2] = scaler[2]

register_constructor(Scale, "scale")

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


class Rotate(VraagTransformation):
    def __init__(self, parent, axis, angle):
        super().__init__(parent)
        self.axis = axis
        self.angle = angle
        self.matrix = rotation_matrix(axis, angle)

register_constructor(Rotate, "rotate")

class Rotator(VraagTransformation):
    def __init__(self, parent, axis, n, radius=1):
        super().__init__(parent)
        self.n = n
        self.radius = radius
        self.axis = axis
    def __iter__(self):
        for i in range(self.n):
            yield self.rotate(self.axis, i*360/self.n)\
                    .translate(right*self.radius)


register_constructor(Rotator, "rotator")
