import time
import sys
import math
from vraag import *
import bpy


V("#Cube").remove()
root = V.construct()

root.cube().difference(root.cylinder(radius=0.4,height=1.2))

p = root.translate([2,0,0])
p.cube().union(p.cylinder(radius=0.4,height=1.2))

p = p.translate([2,0,0])
p.cube().difference(p.cylinder(radius=0.4,height=1.2), apply_modifier=True, keep=False)

