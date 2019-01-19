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
        if bpy.app.version < (2,80):
            scene.objects.link(ob)
        else:
            node = self.get_last_collections_node()
            if node:
                for collection in node._collections:
                    collection.objects.link(ob)
            else:
                scene.collection.objects.link(ob)


        node = self.get_last_layers_node()
        if node is not None:
            ob.layers = [(i in node._layers) for i in range(len(ob.layers))]
        return ob


class Plane(VraagObject):
    def __init__(self, parent, size=(1,1), name="Plane"):
        super().__init__(parent, name)
        self.size = size
        self.name = name
        self.object = self.build()

    def build(self):
        me = bpy.data.meshes.new(self.name)
        size = self.size
        try:
            if len(size)==2:
                sx, sy = size
            else:
                raise TypeError("Size parameter must be a scalar or have two elements")
        except TypeError:
            sx = size
            sy = size

        verts = np.array([[-sx,sy,0],
                         [-sx,-sy,0],
                         [sx,-sy,0],
                         [sx,sy,0]]
                        )/2
        faces = [[0,1,2,3]]

        me.from_pydata(verts, [], faces)
        me.update()

        ob = bpy.data.objects.new(self.name, me)
        self.setup(ob)
        return ob

register_constructor(Plane, "plane")

class Cube(VraagObject):
    def __init__(self, parent, size=1, name="Cube"):
        super().__init__(parent, name)
        self.size = size
        self.object = self.build()

    def build(self):
        me = bpy.data.meshes.new("MyMesh")
        size = self.size
        try:
            if len(size)==3:
                sx, sy, sz = size
            else:
                raise TypeError("Size parameter must be a scalar or have three elements")
        except TypeError:
            sx = size
            sy = size
            sz = size

        verts = np.array([
            [sx, sy, -sz],
            [sx, -sy, -sz],
            [-sx, -sy, -sz],
            [-sx, sy, -sz],
            [sx, sy, sz],
            [sx, -sy, sz],
            [-sx, -sy, sz],
            [-sx, sy, sz],
        ], dtype=np.float) /2

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

class Box(VraagObject):
    def __init__(self, parent, a,b, name="Box"):
        super().__init__(parent, name)
        self.a = a
        self.b = b
        self.object = self.build()

    def build(self):
        me = bpy.data.meshes.new("Box")


        ax, ay, az = self.a
        bx, by, bz = self.b

        verts = np.array([
            [bx, by, az],
            [bx, ay, az],
            [ax, ay, az],
            [ax, by, az],
            [bx, by, bz],
            [bx, ay, bz],
            [ax, ay, bz],
            [ax, by, bz],
        ], dtype=np.float)

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

register_constructor(Box, "box")


class Plane(VraagObject):
    def __init__(self, parent, size=(1,1), name="Plane"):
        super().__init__(parent, name)
        self.size = size
        self.object = self.build()

    def build(self):
        me = bpy.data.meshes.new(self.name)
        a,b = self.size
        a /= 2
        b /= 2
        verts = np.array([
            [-a,-b, 0],
            [-a, b, 0],
            [a, b, 0],
            [a, -b, 0],
        ], dtype=np.float)

        faces = [[0, 1, 2, 3]]
        me.from_pydata(verts, [], faces)
        me.update()

        ob = bpy.data.objects.new(self.name, me)
        
        self.setup(ob)
        return ob

register_constructor(Plane, "plane")

def make_circle_points(n):
    X = np.zeros((n,2), dtype=np.float)
    radians = (2*math.pi / n ) * np.arange(0,n)
    X[:,0] = np.cos(radians)
    X[:,1] = np.sin(radians)
    return X



def parse_height(param):
    try:
        if len(param)==2:
            a,b = param
            return a,b 
    except TypeError:
        return -param/2, param/2
    return param

class Extrude(VraagObject):
    def __init__(self, parent, points, height=1, name="Extrusion"):
        super().__init__(parent, name=name)
        self.points = points
        self.height = height
        self.object = self.build()

    def build(self):
        verts = np.array(self.points, dtype=float)
        if verts.shape[1] != 2:
            raise TypeError("Vertices for extrusion must have two columns.")
        top, bottom = parse_height(self.height)
        n_points = len(self.points)
        poly = np.zeros([n_points,3], dtype=float)
        poly[:, :-1] = verts
        vertices = np.vstack([poly+np.array((0,0,bottom)), poly+np.array((0,0, top))])
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
register_constructor(Extrude, "prism")


class Cylinder(VraagObject):
    def __init__(self, parent, radius=1, height = 1, n_vertices=64, name="Cylinder", cap="polygon"):
        super().__init__(parent, name=name)
        self.n_vertices = n_vertices
        self.radius = radius
        self.height = height
        self.cap = cap
        self.object = self.build()

    def build(self):
        n = self.n_vertices
        circle_points = make_circle_points(n)*self.radius
        top,bottom = parse_height(self.height)
        total_v = n*2 + 2
        vertices = np.zeros((total_v,3))
        upt = up.transpose()
        vertices[0,:] = upt * top
        vertices[1,:] = upt * bottom
        vertices[2:n+2,0] = circle_points[:,0]
        vertices[2:n+2,1] = circle_points[:,1]

        vertices[2:n+2,:] += upt * top
        vertices[n+2:2*n+2,:] = upt *  bottom

        vertices[n+2:2*n+2,0] = circle_points[:,0]
        vertices[n+2:2*n+2,1] = circle_points[:,1]

        me = bpy.data.meshes.new(self.name)

        faces  =[]

        top_face = []
        bottom_face= []
        for i in range(n):
            a = 2+i
            b = 2+(i+1) % n 
            c = n+2+i
            d = n+2+(i+1)%n
            if self.cap=="fan":
                faces.append([0,a,b])
                faces.append([1,c,d])
            elif self.cap=="polygon":
                top_face.append(a)
                bottom_face.append(c)

            faces.append([a,c,d,b])
        if self.cap=="polygon":
            faces.append(top_face)
            faces.append(bottom_face)

        me.from_pydata(vertices, [], faces)
        me.update()

        ob = bpy.data.objects.new(self.name, me)
        self.setup(ob)
        return ob


register_constructor(Cylinder, "cylinder")

class Sphere(VraagObject):
    def __init__(self, parent, radius=1, meridians=20, parallels=20, name="Sphere"):
        super().__init__(parent, name=name)
        self.meridians = meridians
        self.parallels = parallels
        self.radius = radius
        self.object = self.build()

    def build(self):
        """ ported from https://github.com/caosdoar/spheres/blob/master/src/spheres.cpp """
        me = bpy.data.meshes.new("UVSphere")
        meridians = self.meridians
        parallels = self.parallels
        r = self.radius

        verts = []
        faces = []

        verts.append((0,0,r))
        for j in range(parallels-1):
            polar = math.pi * (j+1) / parallels
            sp  = math.sin(polar)
            cp = math.cos(polar)

            for i in range(meridians):
                azimuth = 2.0 * math.pi * i / meridians
                sa = math.sin(azimuth)
                ca = math.cos(azimuth)

                z = r*cp
                x = r*sp*sa
                y = r*sp * ca
                verts.append((x,y,z))
        verts.append((0,0,-r))


        for j  in range(parallels-2):
            aStart = j * meridians + 1
            bStart = (j+1) * meridians + 1 

            for i in range(meridians):
                a = aStart + i
                a1 = aStart + (i + 1) % meridians
                b = bStart + i
                b1 = bStart + (i + 1) % meridians
                faces.append((a,a1,b1,b))

        for i in range(meridians):
            a = i + 1
            b = (i + 1) % meridians + 1
            faces.append((0,b,a))

        for i in range(meridians):
            a = i +  meridians * (parallels - 2) + 1
            b = (i + 1) % meridians + meridians * (parallels - 2) + 1
            faces.append((len(verts)-1,a,b))

        me.from_pydata(verts, [], faces)
        me.update()


        ob = bpy.data.objects.new(self.name, me)
        self.setup(ob)
        return ob


register_constructor(Sphere, "sphere")

class Empty(VraagObject):
    def __init__(self, parent, draw_size=1, draw_type="PLAIN_AXES", name="Empty"):
        super().__init__(parent, name=name)
        
        self.draw_size = draw_size
        self.draw_type = draw_type
        self.object = self.build()

    def build(self):
        ob = bpy.data.objects.new(self.name, None)
        #ob.empty_draw_size=self.draw_size
        #ob.empty_draw_type=self.draw_type
        self.setup(ob)
        return ob

register_constructor(Empty, "empty")

class Mesh(VraagObject):
    def __init__(self, parent, source, library=None, name="LinkedMesh", linked=True):
        super().__init__(parent, name=name)
        self.source = source
        self.library = library
        self.linked = linked
        self.object = self.build()

    def find_mesh_locally(self, source):
        if type(source) is bpy.types.Mesh:
            return source
        if type(source) is bpy.types.Object:
            return source.data
        try:
            mesh = bpy.data.meshes[source]
            return mesh
        except KeyError:
            pass
        try: 
            mesh = bpy.data.objects[source].data
            return mesh
        except KeyError:
            raise KeyError("No mesh or object called '{self.source}' found".format(self=self))
    def build(self):
        if self.library is None:
            mesh = self.find_mesh_locally(self.source)
        else:
            with bpy.data.libraries.load(self.library, relative=True, link=True) as (data_from, data_to):
                    data_to.meshes = [self.source]
            mesh = data_to.meshes[0]
        if not self.linked:
            mesh = mesh.copy()
        ob = bpy.data.objects.new(self.name, mesh)
        self.setup(ob)
        return ob

register_constructor(Mesh, "mesh")

class STL(VraagObject):
    def __init__(self, parent, filename, name=None):
        super().__init__(parent, name=name)
        self.filename = filename
        if name is None:
            self.name = filename
        else:
            self.name = name
        self.object = self.build()

    def build(self):
        from io_mesh_stl.stl_utils import read_stl
        faces, normals,vertices = read_stl(self.filename)
        me = bpy.data.meshes.new(self.name)
        me.from_pydata(vertices, [], faces)
        me.update()
        ob = bpy.data.objects.new(self.name, me)
        self.setup(ob)
        return ob

register_constructor(STL, "stl")
