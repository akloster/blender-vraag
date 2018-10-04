import numpy as np
import math
from vraag import *
import bpy


n, m = 40,40
d = 0.4
xs, ys = 2*d,2*d # strings
xh, yh = 2*d,2*d # holes
x_spacing, y_spacing = xs+xh, ys+yh
x_size = x_spacing*n
y_size = y_spacing*m

def gi(i,j):
    return i*m+j

verts_tl = []
verts_tr = []
verts_dr = []
verts_dl = []


xm = x_size / 2
ym = y_size / 2
for i in range(n):
    for j in range(m):
        x = i*x_spacing-xm
        y = j*y_spacing-ym

        verts_tl.append((x,y,0))
        verts_tr.append((x+xh,y,0))
        verts_dr.append((x+xh,y+yh,0))
        verts_dl.append((x,y+yh,0))


verts = verts_tl + verts_tr + verts_dr + verts_dl
faces = []
tl, tr, dr, dl = [i*n*m for i in range(4)]
for i in range(n):
    for j in range(m):
        if (i>0):
            faces.append([tl+gi(i,j),
                          dl+gi(i,j),
                          dr+gi(i-1,j),
                          tr+gi(i-1,j)
                         ])
            if j>0:
                faces.append([tl+gi(i,j),
                             tr+gi(i-1,j),
                              dr+gi(i-1,j-1),
                              dl+gi(i,j-1)
                             ])
        if (j>0):
            faces.append([tl+gi(i,j),
                          dl+gi(i,j-1),
                          dr+gi(i,j-1),
                          tr+gi(i,j)
                         ])
V("#Cube").hide()
mesh = bpy.data.meshes.new("Mesh")
mesh.from_pydata(verts, [], faces)
mesh.update()
ob = bpy.data.objects.new("Mesh", mesh)
bpy.context.scene.objects.link(ob)
mod = ob.modifiers.new("Test", "SOLIDIFY")
mod.thickness = 0.2
mod.offset = 1
