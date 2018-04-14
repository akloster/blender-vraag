import time
import sys
import math
from vraag import *
import bpy


V("#Cube").remove()
root = V.construct()

sphere = root\
        .sphere(meridians=128, parallels=128)

for pos in root.rotator(n=6, radius=0.65, axis=up):
    sphere.difference(pos.cylinder(radius=0.2, height=3-0.2, n_vertices=64))

for pos in root.rotator(n=6, radius=1, axis=up):
    sphere.difference(pos.sphere(radius=0.3, meridians=64, parallels=64)) 
