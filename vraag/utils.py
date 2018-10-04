import numpy as np
import bpy
import math

def vector(*v):
    a = np.array(v, dtype=np.float)
    a.shape = (len(v),1)
    return a


identity = lambda: np.identity(4, dtype=np.float)

up = vector(0,0,1) 
right = vector(1,0,0)
left = vector(-1,0,0)
down = vector(0,0,-1)
front = vector(0,-1,0)
back = vector(0,1,0)
forward = back
backward = front
backwards = front
def rotation_matrix(axis, angle):
    """ generate rotation matrix from axis/angle.
        Code taken from Stack Overflow
    """

    theta = angle/360*math.pi
    axis = np.array(axis, dtype=np.float)
    axis /= np.linalg.norm(axis)
    a = math.cos(theta)
    b, c, d = -axis*math.sin(theta)
    aa, bb, cc, dd = a*a, b*b, c*c, d*d
    bc, ad, ac, ab, bd, cd = b*c, a*d, a*c, a*b, b*d, c*d
    return np.array([[aa+bb-cc-dd, 2*(bc+ad), 2*(bd-ac),0],
                     [2*(bc-ad), aa+cc-bb-dd, 2*(cd+ab),0],
                     [2*(bd+ac), 2*(cd-ab), aa+dd-bb-cc,0],
                     [0,0,0,1]], dtype=np.float)

def find_materials(*args):
    for arg in args:
        if isinstance(arg, str):
            yield bpy.data.materials[arg]

        try:
            yield from find_materials(list(iter(arg)))
        except TypeError as te:
            pass

def walk_collections(collection=None):
    if collection is None:
        collection = bpy.context.collection
    yield collection
    for child in collection.children:
        yield from walk_collections(child)

def find_collections(*args):
    for arg in args:
        if isinstance(arg, str):
            for coll in walk_collections():
                if coll.name==arg:
                    yield coll
            continue

        if isinstance(arg, bpy.types.Collection):
            yield arg
            continue
        try:
            yield from find_collections(*arg)
        except TypeError as te:
            pass

