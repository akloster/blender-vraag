import numpy as np
from vraag.utils import * 

def vector4(v):
    try:
        if len(v.shape)==2:
            if (v.shape[0]>1) and (v.shape[1]>2):
                raise TypeError("Vectors must not have two dimensions")
            v.shape = v.shape[0]
    except AttributeError:
        pass

    if len(v)==3:
        p = np.zeros(4, np.float32)
        p[:3] = v
        p[3] = 1
    elif len(v)==4:
        p = np.array(v).astype(np.float32)
    else:
        raise TypeError("Need a parameter with 3 or 4 elements.")
    return p

def translation_matrix(v):
    tm = identity()
    tm[3,:3] = vector4(v)[:3]
    return tm

class TurtlePoint(object):
    def __init__(self, parent=None, new_transformation=None):
        self.parent = parent
        if parent is None:
            self.transformation = identity()
        else:
            self.transformation = new_transformation.copy()
    def copy(self):
        return TurtlePoint(self, self.transformation)

    @property
    def location(self):
        return self.transform_point((0,0,0))

    def transform_point(self, v):
        return np.dot(vector4(v), self.transformation)

    def translate(self, v):
        tm = translation_matrix(vector4(v))
        tm = np.dot(tm, self.transformation)
        return TurtlePoint(self, tm)

    def scale(self, f):
        try:
            if len(f)!=3:
                raise ValueError("Scaling factor must be scalar or a 3D vector")
            tm = np.diag(vector4(f))
        except TypeError:
            tm = np.diag(np.repeat(f,4))
        tm[3,3] = 1
        return TurtlePoint(self, np.dot(tm, self.transformation))




    def move(self, v, steps=1):
        for i in range(1,steps+1):
            tm = translation_matrix(vector4(v)/steps * i)
            tm = np.dot(tm, self.transformation)
            yield TurtlePoint(self, tm)
        tm = translation_matrix(v)
        tm =  np.dot(tm, self.transformation)
        return TurtlePoint(self, tm)

    def rotate(self, axis, angle):
        tm = rotation_matrix(axis, angle)
        tm = np.dot(tm, self.transformation)
        return TurtlePoint(self, tm)

    def turn(self, axis, angle, radius=1, forward=forward, steps = 1,
             screw=0):
        t = self
        _forward = vector4(forward)[:3]
        _axis = vector4(axis)[:3]
        n = np.cross(axis, forward)
        
        center = vector4(n)*radius
        center[3] = 1
        for i in range(1, steps+1):
            tm = translation_matrix(_axis*(screw/steps)*i)
            tm = np.dot(tm, translation_matrix(center[:3]))
            rot = rotation_matrix(_axis, angle/steps * i)
            tm = np.dot(tm, rot)
            tm = np.dot(tm, translation_matrix(-center[:3]))
            tm = np.dot(tm, self.transformation)
            t = self.__class__(t,tm)
            yield t
        return t


def turtle_extrusion_mesh(vertices, edges,  points):
    vertices = np.hstack((vertices, np.ones((vertices.shape[0],1))))
    m = len(vertices)
    verts = []
    faces = []

    for i, point in enumerate(points):
        tm = point.transformation
        vs = np.dot(vertices, tm)
        for x,y,z,t in vs:
            verts.append((x,y,z))
        if i == 0:
            continue
        for a,b in edges:
            faces.append((i*m+a,i*m+b, (i-1)*m+b, (i-1)*m+a))
    return verts, faces
