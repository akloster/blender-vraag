"""
    This is a script to create 3D printable nets/grids/meshes.

    I needed some ventilation for a couple of insect enclosures. Now there is plenty of
    commercially available options, but I decided to try and print them out of PLA or PETG.
    This would mean I can control the properties of the material more closely, and I don't
    need to have big rolls of the stuff lying around. A clear example of inefficient 3d
    printing over kill, but still efficient enough to beat some alternatives.

    Anyway, the straight solution would be to create a box with holes, either by CSG or
    through manually creating the geometry. Unfortunately, slicing such objects with Cura
    results in a very inefficient printing process. Instead of running straight rows and
    columns, the slicer would try to trace around individual holes, wasting time on
    unneccessary accelerations and travel. And from the point of the slicer, this is
    clearly the right way to do. In almost any other situation we don't want to let the
    nozzle extrude plastic in a place there is already plastic, namely the row/column
    intersections.

    My next idea was to create custom gcode to do exactly this. I'm not getting good results
    on my attempts so far, but this may be the ultimate solution.

    Meanwhile I tried to cheat Cura. This script creates columns and rows as individual boxes,
    but it interleaves columns and rows layer by layer. The boxes are 0.2mm in height.
    In the actual exported mesh, there are gaps between each of the column layers and between
    each ofthe row layers. But this doesn't matter a lot in practice, because the plastic
    gets fused anyway. Especially with a higher flow rate.

    The result isn't perfect, but it works surprisingly well. The nets are strong enough for
    my needs, and print relatively quickly.
    
    Print settings:
        - Layer height should be 0.2 (or whatever you set it to in this script)
        - You need to make sure all parts of the model are treated as walls. Depending on
          your parameter adjustments, you need to increase the wall thickness.
        - you can crank up the speed as high as you can get a good first layer adhesion with
        - first layer adhesion is more important than beauty here, so higher temperatures
          are recommended.
        - the prints are almost designed for maximum warping. I found it's best to let the
          print cool on the bed before removing it.

"""



import numpy as np
import math
from vraag import *
import bpy


# Nozzle diameter
d = 0.4
# Number of grid/column layers, the actual number of layers is double this number
layers = 3

# String width
xs, ys = 1*d,1*d # strings
# Gap width
xh, yh = 1,1
x_spacing, y_spacing = xs+xh, ys+yh

x_size = 130
y_size = 70
n, m = round(y_size/y_spacing),round(x_size/x_spacing)
layer_height = 0.2

V("#Cube").remove()

root = V.construct()

for layer in range(layers):
    pos = root.translate((0, -y_size/2, 2*layer*layer_height))
    for i in range(n+1):
        pos.translate((0,i*y_spacing,0)).cube((x_size,ys+0.01,layer_height))

    pos = root.translate((-x_size/2, 0, 2*layer*layer_height+layer_height))
    for i in range(m+1):
        pos.translate((i*x_spacing,0,0)).cube((xs+0.01,y_size,layer_height))


