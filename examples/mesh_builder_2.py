import bpy
from vraag import *
from vraag.construct.turtle import *
from vraag.construct.mesh_builder import pipe
from vraag.utils import *
import numpy as np
from copy import deepcopy
from functools import reduce
import math

V("Cube").remove()
e = 0.0001
resolution = 2**7
root = V.construct()

def lcm(a, b):
    return a * b // math.gcd(a, b)

def cross_section(corners = 3, n=16,m=16):
    r = 0.1
    a = 1
    t = TurtlePoint().translate((a/2,0,0))
    for i in range(corners):
        t = yield from t.move(forward*a/2, steps=math.floor(n/2))
        t = yield from t.turn((0,0,1), 360/corners, steps=m, radius=r)
        t = yield from t.move(forward*a/2, steps=math.ceil(n/2))

def path():
    t = TurtlePoint()
    a, b = 3, 10
    n = reduce(lcm,range(a,b), 1)
    print("->", n)
    vertical = t.move((0,0,10), steps=(b-a+1))
    first = True
    for corners,t in zip(reversed(range(a,b)), [t]+list(vertical)):
        vertices = [v.origin for v in cross_section(corners, n//corners, n//corners)]
        va = np.array(vertices)[:,:3]
        t.data.update(vertices=va-va.mean(axis=0))
        f = corners*0.25
        if first:
            for i in reversed(range(1,4)):
                yield t.scale((f/i,f/i,1))
            for i in range(5):
                yield t.scale((f,f,1))
            first = False
        yield t.scale((f,f,1))

    yield t.scale((f,f,1))
    for i in range(1,4):
        yield t.scale((f/i,f/i,1))

mesh = pipe(path()).make_mesh()
root.mesh(mesh)
