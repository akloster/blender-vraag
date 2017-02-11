import time
import sys
import math
from vraag import *
import bpy


V("#Cube").remove()
root = V.construct()


base = root.cylinder(radius=1,height=0.5)
middle = root.translate(up*1.5).cylinder(radius=1,height=0.5)        
top = root.translate(up*1.5*2)\
        .cylinder(radius=1,height=0.5)
rotator = root.translate(up*1.5).rotator(n=5, radius=0.65, axis=up)
for pos in rotator:
    pos.cylinder(radius=0.2, height=3-0.2)

middle.union(rotator, base, top, apply_modifier=True, keep=False)

