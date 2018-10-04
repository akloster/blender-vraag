import time
import sys
import math
from vraag import *
import bpy

# This doesn't quite work on 2.8 yet, because materials have gotten more complicated!
def simple_material(name, diffuse):
    mat = bpy.data.materials.new(name)
    mat.diffuse_color = diffuse
    mat.diffuse_shader = 'LAMBERT' 
    mat.diffuse_intensity = 1.0 
    return mat

red_material = simple_material("red", [1,0,0]) 
yellow_material = simple_material("yellow", [1,1,0]) 
green_material = simple_material("green", [0,1,0]) 
V("Cube").remove()
root = V.construct()

root.material(green_material)\
        .cube()\
        .translate([0,0,1])\
        .material(yellow_material)\
        .cube()\
        .translate([0,0,1])\
        .material(red_material)\
        .cube()
