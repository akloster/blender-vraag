import time
import sys
import math
from vraag import *
import bpy


V("Cube").remove()
root = V.construct()


# Create 10 cubes rotating around an "Empty" object
empty = root.empty()
for position in empty.rotator(axis=up, n=10, radius=4):
    position.cube()

