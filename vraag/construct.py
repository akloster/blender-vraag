import numpy as np
import math
import bpy
from vraag.utils import *


identity = lambda: np.identity(4, dtype=np.float)


class VraagConstruct(object):
    """ Baseclass for all construction nodes."""
    def __init__(self, parent=None):
        self.parent = parent
        self.children = []
        self.matrix = identity() 
        self.object = None

    def add_child(self, obj):
        self.children.append(obj)

    def cube(self, size=[1,1,1]):
        obj = Cube(self, size)
        self.add_child(obj)
        return obj


    def cylinder(self, radius=1, height=1):
        obj = Cylinder(self, radius, height)
        self.add_child(obj)
        return obj

    def empty(self, **kwargs):
        obj = Empty(self, **kwargs)
        self.add_child(obj)
        return obj

    def calculate_local_matrix(self):
        """ Calculate the local transformation matrix
            by working up the chain until the next object
        """
        m = self.matrix
        p = self
        while p.parent:
            p = p.parent
            if p.object:
                # stop at next object
                break
            m = m.dot(p.matrix)
        return m
    
    def find_child_objects(self):
        return list(set(self._find_child_objects()))

    def _find_child_objects(self):
        for child in self.children:
            if child.object:
                yield child.object
            else:
                yield from child._find_child_objects()

    def translate(self, v):
        obj = Translate(self,v)
        self.add_child(obj)
        return obj

    def rotate(self, axis, angle):
        obj = Rotate(self,axis,angle)
        self.add_child(obj)
        return obj

    def scale(self, *args):
        obj = Scale(self,*args)
        self.add_child(obj)
        return obj
    
    def build(self):
        return None

    def get_parent_object(self):
        p = self.parent
        while p.parent:
            if p.object:
                return p.object
            p = p.parent

    def union(self, target, *targets, **kwargs):
        obj = Union(self, target, *targets, **kwargs)
        return obj

    def difference(self, target, *targets, **kwargs):
        obj = Difference(self, target, *targets, **kwargs)
        return obj


    def intersection(self, target, *targets, **kwargs):
        obj = Intersection(self, target, *targets, **kwargs)
        return obj

    def rotator(self, axis, n, radius=1): 
        obj = Rotator(self, axis, n, radius)
        self.add_child(obj)
        return obj

    def material(self, material):
        obj = Material(self, material)
        self.add_child(material)
        return obj

    def get_last_material_node(self):
        node = self.parent

        while node:
            if hasattr(node, "_material"):
                return node
            node = node.parent

        return None


class VraagObject(VraagConstruct):
    def __init__(self, parent, name=None):
        super().__init__(parent)
        self.name = name

    def setup(self, ob):
        scn = bpy.context.scene
        scn.objects.link(ob)
        scn.objects.active = ob
        ob.select = True
        ob.parent = self.get_parent_object() 
        ob.matrix_local = self.calculate_local_matrix()
        ob.name = self.name
        if (ob.type =="MESH"):
            node = self.get_last_material_node()
            if node:
                ob.data.materials.append(node._material)
        return ob

class Cube(VraagObject):
    def __init__(self, parent, size, name="Cube"):
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


def make_circle_points(n):
    X = np.zeros((n,2), dtype=np.float)
    radians = (2*math.pi / n ) * np.arange(0,n)
    X[:,0] = np.cos(radians)
    X[:,1] = np.sin(radians)
    return X


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


class VraagTransformation(VraagConstruct):
    def __init__(self, parent):
        super().__init__(parent)
        self.matrix = identity()
        


class Translate(VraagTransformation):
    def __init__(self, parent, v):
        super().__init__(parent)
        v = np.array(v, dtype=np.float)
        self.v = v
        self.matrix[3,0:3] = v.transpose()

class Scale(VraagTransformation):
    def __init__(self, parent, *args):
        super().__init__(parent)
        if len(args)==1:
            scaler=[args]
            try:
                if len(args[0]):
                    scaler = args[0]
            except TypeError:
                if len(args):
                    scaler = args
        else:
            scaler = args
        if len(scaler)==1:
            self.matrix[0,0] = scaler[0]
            self.matrix[1,1] = scaler[0]
            self.matrix[2,2] = scaler[0]
        else:
            self.matrix[0,0] = scaler[0]
            self.matrix[1,1] = scaler[1]
            self.matrix[2,2] = scaler[2]


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


class Rotate(VraagTransformation):
    def __init__(self, parent, axis, angle):
        super().__init__(parent)
        self.axis = axis
        self.angle = angle
        self.matrix = rotation_matrix(axis, angle)


class VraagBoolean(VraagConstruct):
    def __init__(self, parent, target, *targets,**kwargs):
        super().__init__(parent) 
        self.target = target
        self.apply_modifier = kwargs.get("apply_modifier", False)
        self.keep = kwargs.get("keep", True)

        obj = self.parent.object
        bpy.context.scene.objects.active = obj
         
        if targets:
            targets =[target] + list(targets)
        else:
            targets = [target]

        objects = sum((_target.find_child_objects() for _target in targets), [node.object for node in targets if node.object])
        for obj in objects:
            mod = self.parent.object.modifiers.new (name='bool.001', type="BOOLEAN")
            mod.operation = self.operation
            mod.object = obj
            if self.apply_modifier:
                # Using an operator for this, and a string name to reference the modifier
                # seems wrong and broken. Haven't found a better way though
                result = bpy.ops.object.modifier_apply(modifier=mod.name)
                if not self.keep:
                    bpy.data.objects.remove(obj, do_unlink=True)

class Union(VraagBoolean):
    operation = "UNION"

class Difference(VraagBoolean):
    operation = "DIFFERENCE"

class Intersection(VraagBoolean):
    operation = "INTERSECTION"


class Rotator(VraagTransformation):
    def __init__(self, parent, axis, n, radius=1):
        super().__init__(parent)
        self.n = n
        self.radius = radius
        self.axis = axis
    def __iter__(self):
        for i in range(self.n):
            yield self.rotate(self.axis, i*360/self.n)\
                    .translate(right*self.radius)

class Material(VraagObject):
    def __init__(self, parent, material):
        super().__init__(parent)
        self._material = material


