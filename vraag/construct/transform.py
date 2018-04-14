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
    def __init__(self, parent, v, y=0,z=0):
        super().__init__(parent)
        try:
            if len(v)!=3:
                v = v,y,z
        except TypeError:
            v = v, y, z

        v = np.array(v, dtype=np.float)[:3]
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
