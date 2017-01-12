import time
import sys
import math
from vraag import *
import bpy


V("#Cube").remove()
root = V.construct()

root.scale(2).translate([0,0,1]).rotate(up,45).rotate(right, 45) .cube()

