import numpy as np
import math
from vraag import *
import bpy


# Nozzle diameter. The "fudge factor" tricks Cura into actually slicing the lines
d = 0.4
# Number of grid/column layers, the actual number of layers is double this number
layers = 5

# String width
xs, ys = 1*d,1*d # strings
# Gap width
xh, yh = 1.5, 1.5
x_spacing, y_spacing = xs+xh, ys+yh
#x_size = x_spacing*n
#y_size = y_spacing*m

x_size = 130
y_size = 70
n, m = round(y_size/y_spacing),round(x_size/x_spacing)
layer_height = 0.2

V("#Cube").remove()

root = V.construct()

for layer in range(layers):
    pos = root.translate((0, -y_size/2, 2*layer*layer_height))
    for i in range(n+1):
        pos.translate((0,i*y_spacing,0)).cube((x_size,ys+0.1,layer_height))

    pos = root.translate((-x_size/2, 0, 2*layer*layer_height+layer_height))
    for i in range(m+1):
        pos.translate((i*x_spacing,0,0)).cube((xs+0.1,y_size,layer_height))

