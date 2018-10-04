import time
import sys
import math
from vraag import *
import bpy


V("Cube").remove()
root = V.construct()

scene = bpy.data.scenes.new("Scene2")
root.scene("Scene2").cube(2)
root.scene(bpy.context.scene).cylinder(2)
