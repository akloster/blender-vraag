import bpy
from vraag import *
from vraag.construct.turtle import *
from vraag.construct.mesh_builder import extrude2
from vraag.utils import *
import numpy as np
from copy import deepcopy

V("Cube").remove()
e = 0.0001
resolution = 2**7
root = V.construct()


def test():
    t = TurtlePoint().translate((0,1.5,0))
    r = 1.5
    t = yield from t.turn((0,0,1), 310, steps=200, radius=r)
    t = yield from t.move(forward*.5, steps=10) 
    t = yield from t.turn((0,0,-1), 250, steps=200, radius=r)
    t = yield from t.move(forward*.5, steps=10)
    t = yield from t.turn((0,0,1), 310, steps=200, radius=r)

def test3():
    t = TurtlePoint()


def test2():
    t = TurtlePoint()
    yield from t.move((0,0,4),steps=1)
    #yield from t.turn((1,0,0)

mesh= extrude2(test(), test2(), width=0.1).make_mesh()
root.mesh(mesh)

