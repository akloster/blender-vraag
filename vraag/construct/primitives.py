import numpy as np
import math
import bpy
from vraag.utils import *
from .base import VraagConstruct, register_constructor


class VraagObject(VraagConstruct):
    def __init__(self, parent, name=None):
        super().__init__(parent)
        self.name = name

    def setup(self, ob):
        ob.select = True
        ob.parent = self.get_parent_object() 
        ob.matrix_local = self.calculate_local_matrix()
        ob.name = self.name
        if (ob.type =="MESH"):
            node = self.get_last_material_node()
            if node:
                ob.data.materials.append(node._material)
        node = self.get_last_scene_node()
        if node is None:
            scene = bpy.context.scene
        else:
            scene = node._scene
        scene.objects.link(ob)
        scene.objects.active = ob
        return ob

class Cube(VraagObject):
    def __init__(self, parent, size=1, name="Cube"):
        super().__init__(parent, name)
        self.size = size
        self.object = self.build()

    def build(self):
        me = bpy.data.meshes.new("MyMesh")

        verts = np.array([
            [1, 1, -1],
            [1, -1, -1],
            [-1, -1, -1],
            [-1, 1, -1],
            [1, 1, 1],
            [1, -1, 1],
            [-1, -1, 1],
            [-1, 1, 1],
        ], dtype=np.float)*(np.asarray(self.size)/2)

        faces = [
            [0, 1, 2, 3],
            [4, 7, 6, 5],
            [0, 4, 5, 1],
            [1, 5, 6, 2],
            [2, 6, 7, 3],
            [4, 0, 3, 7],
        ]
        me.from_pydata(verts, [], faces)
        me.update()

        ob = bpy.data.objects.new(self.name, me)
        self.setup(ob)
        return ob


register_constructor(Cube, "cube")

def make_circle_points(n):
    X = np.zeros((n,2), dtype=np.float)
    radians = (2*math.pi / n ) * np.arange(0,n)
    X[:,0] = np.cos(radians)
    X[:,1] = np.sin(radians)
    return X


class Extrude(VraagObject):
    def __init__(self, parent, points, height=1, name="Extrusion"):
        super().__init__(parent, name=name)
        self.points = points
        self.height = height
        self.build()

    def build(self):
        verts = np.array(self.points, dtype=float)
        if verts.shape[1] != 2:
            raise TypeError("Vertices for extrusion must have two columns.")
        n_points = len(self.points)
        poly = np.zeros([n_points,3], dtype=float)
        poly[:, :-1] = verts
        delta_z = np.zeros(poly.shape)
        delta_z[:,2]= self.height/2.0
        vertices = np.vstack([poly+delta_z, poly-delta_z])
        faces = [np.arange(0,len(poly), dtype=int)]
        faces.append(faces[0][::-1]+len(poly))

        for i in range(n_points):
            face = [i,(i+1) % n_points, n_points+ (i+1)% n_points, i+n_points]
            faces.append(face)

        me = bpy.data.meshes.new(self.name)
        
        me.from_pydata(vertices, [], faces)
        me.update()

        ob = bpy.data.objects.new(self.name, me)
        scn = bpy.context.scene
        self.setup(ob)
        return ob

register_constructor(Extrude, "extrude")

class Cylinder(VraagObject):
    def __init__(self, parent, radius=1, height = 1, n_vertices=30, name="Cylinder"):
        super().__init__(parent, name=name)
        self.n_vertices = n_vertices
        self.radius = radius
        self.height = height
        self.object = self.build()


    def build(self):
        n = self.n_vertices
        circle_points = make_circle_points(n)*self.radius
        total_v = n*2 + 2
        vertices = np.zeros((total_v,3))
        upt = up.transpose()
        vertices[0,:] = upt * self.height/2
        vertices[1,:] = -upt * self.height/2
        vertices[2:n+2,0] = circle_points[:,0]
        vertices[2:n+2,1] = circle_points[:,1]

        vertices[2:n+2,:] += upt * (self.height/2)
        vertices[n+2:2*n+2,:] -= upt *(self.height/2)

        vertices[n+2:2*n+2,0] = circle_points[:,0]
        vertices[n+2:2*n+2,1] = circle_points[:,1]

        me = bpy.data.meshes.new(self.name)

        faces  =[]

        for i in range(n):
            a = 2+i
            b = 2+(i+1) % n 
            c = n+2+i
            d = n+2+(i+1)%n
            faces.append([0,a,b])
            faces.append([1,c,d])

            faces.append([a,c,d,b])

        me.from_pydata(vertices, [], faces)
        me.update()

        ob = bpy.data.objects.new(self.name, me)
        scn = bpy.context.scene
        self.setup(ob)
        return ob


register_constructor(Cylinder, "cylinder")

class Empty(VraagObject):
    def __init__(self, parent, draw_size=1, draw_type="PLAIN_AXES", name="Empty"):
        super().__init__(parent, name=name)
        
        self.draw_size = draw_size
        self.draw_type = draw_type
        self.object = self.build()

    def build(self):
        ob = bpy.data.objects.new(self.name, None)
        ob.empty_draw_size=self.draw_size
        ob.empty_draw_type=self.draw_type
        self.setup(ob)
        return ob

register_constructor(Empty, "empty")
