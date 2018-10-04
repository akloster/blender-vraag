import time
import sys
import math
from vraag import *
import bpy
import numpy as np


V("Cube").remove()
root = V.construct()


pos = root

def subdivide(pos, side=3):
    if side<1/3:
        pos.cube(size=side-0.0001)
        return

    positions = [
                 [1,0,1],
                 [1,1,0],
                 [0,1,1],
                 [1,1,1],

                 [-1,0,-1],
                 [-1,-1,0],
                 [0,-1,-1],
                 [-1,-1,-1],

                 [-1, 0,1],
                 [-1, 1,1],
                 [1, 0,-1],
                 [1, 1,-1],
                 [1, -1,-1],
                 [-1, -1,1],
                 [-1, 1,-1],
                 [1, -1,1],
                 [1, -1, 0],
                 [0, -1, 1],
                 [-1, 1, 0],
                 [0, 1, -1],
                ]

    for p in positions:
        subdivide(pos.translate(np.array(p)*side/3), side=side/3)

print("Warning: This may take a while...")
subdivide(pos)

