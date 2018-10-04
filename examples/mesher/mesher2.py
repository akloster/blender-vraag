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
xh, yh = 1, 1
x_spacing, y_spacing = xs+xh, ys+yh
#x_size = x_spacing*n
#y_size = y_spacing*m

x_size = x_spacing * 8
y_size = y_spacing * 8
n, m = np.ceil((y_size-yh)/y_spacing),np.ceil((x_size-xh)/x_spacing)
print(n,m)
layer_height = 0.2

V("#Cube").remove()

root = V.construct()

horizontal_y1 = np.arange(0, n)*y_spacing
horizontal_y2 = horizontal_y1+ys
print(horizontal_y1)
print(horizontal_y2)
vertical_x1 = np.arange(0, m)*x_spacing
vertical_x2 = vertical_x1 +xs

root.box()
#for layer in range(layers):
