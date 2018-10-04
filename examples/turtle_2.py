import bpy
from vraag import *
from vraag.construct.turtle import *
from vraag.utils import *
import numpy as np

V("Cube").remove()
root = V.construct()
def rounded_polygon(n=3):
    a = 1
    b = 0.2
    t = TurtlePoint()
    for i in range(n):
        t = yield from t.move(forward*a, steps=5)
        t = yield from t.turn(up, 360/n,radius=b, steps=15)

def to_2d(iterator):
    for t in iterator:
        print(t.location)
        x,y,z,_ = t.location
        yield x,y

start = root.rotate(right, 90).translate(left*3*3)
for i, n in enumerate(range(3,9)):
    points = np.array(list(to_2d(rounded_polygon(n))))
    x = points[:,0]
    min_x, max_x = np.min(x), np.max(x)
    points[:,0] -= (max_x+min_x)/2
    y = points[:,1]
    min_y, max_y = np.min(y), np.max(y)
    points[:,1] -= (max_y + min_y)/2
    start.translate(right*3*i).prism(points, height=0.2)

