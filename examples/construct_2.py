import time
import sys
import math
from vraag import *
import bpy


V("#Cube").remove()
root = V.construct()
p = root

for i in range(10):
    p = p.translate(right*2).rotate(up, 36).cube()


