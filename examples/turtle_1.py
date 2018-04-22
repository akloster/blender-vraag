import bpy
from vraag import *
from vraag.construct.turtle import *
from vraag.utils import *
import numpy as np

V("#Cube").remove()
root = V.construct()
def tests():
    t = TurtlePoint()
    yield t

    t = yield from t.move(forward, steps=5)
    t = yield from t.turn(up, 90,radius=1, steps=10)
    t = yield from t.move(forward, steps=10)
    t = yield from t.turn(up, 90,radius=1, steps=10)
    t = yield from t.turn(left, 90,radius=1, steps=10)
    t = yield from t.move(forward, steps=5)
    t = yield from t.turn(right, 90,radius=1, steps=10)
    t = yield from t.turn(up, 90,radius=1, steps=10)
    t = yield from t.turn(down, 90,radius=1, steps=10)
    t = yield from t.turn(up, 360*2,radius=1, steps=40, screw=-3)

a = 0.025
vertices = np.array([(-a, 0, a/2), (a,0, a/2), (a,0, -a/2), (-a,0,-a/2)])
edges = [(0,1), (1,2), (2,3),(3,0)]
verts, faces = turtle_extrusion_mesh(vertices, edges, tests())

me = bpy.data.meshes.new("MyMesh")
me.from_pydata(verts, [], faces)
me.update()
extruded = root.mesh(me, name="Extruded")
for out in tests():
    cube = extruded.cube(size=0.1)
    cube.object.matrix_local = out.transformation
