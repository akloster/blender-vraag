import numpy as np
import math
from vraag import *
import bpy


root = V.construct().rotate(right,180)
e = 0.001
w, h, d = 18, 10, 14
t = 1.2
knob = root.box((-w/2,-h/2,0),(w/2,h/2,d))
knob.difference(root.box((-w/2+t,-h/2+t,0-e), (w/2-t, h/2-t, d-t)))
struts = (-0.21,-h/2+e,2),(0.21, h/2-e, d-e)
knob.union(root.translate(left*1.3).box(*struts),
           root.translate(right*1.3).box(*struts))
knob.union(root.box((-w/2+e,-0.4-e,7),(w/2-e, 0.4+e, d-e)))
