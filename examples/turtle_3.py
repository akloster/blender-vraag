import bpy
from vraag import *
from vraag.construct.turtle import *
from vraag.utils import *
import numpy as np

V("#Cube").remove()
root = V.construct()


def fractal(start=None, level=1):
    f = 1/3
    α = 60
    if start is None:
        a = TurtlePoint()
    else:
        a = start.copy()
    yield a
    if level > 0:
        yield from fractal(a.scale(f), level-1)
    b = a.translate(f*right)
    yield b
    c = b.rotate(down, α)
    if level > 0:
        yield from fractal(c.scale(f), level-1)
    c = c.translate(f*right)
    yield c
    d = c.rotate(up, α*2)
    
    if level > 0:
        yield from fractal(d.scale(f), level-1)
    d = d.translate(f*right)
    yield d
    e = d.rotate(down, α)
    if level > 0:
        yield from fractal(e.scale(f), level-1)
    e = e.translate(f*right)
    #yield e
    
    #e = yield from a.move(3*f*right,steps=1)
    #return e

def to_2d(iterator):
    for t in iterator:
        x,y,z,_ = t.location
        yield x,y

side = TurtlePoint().rotate(down,60)
points =[]
for i in range(3):
    points += list(to_2d(fractal(side,level=5)))
    side = side.translate(right).rotate(up, 60*2)

points = np.array(points)
points[:,0]-= 0.5
points[:,1]-= points[:,1].max() / 3
root.rotate(right,90).scale(5).prism(points, height=0.1)
