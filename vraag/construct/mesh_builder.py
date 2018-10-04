import bpy
from vraag import *
from vraag.construct.turtle import *
from vraag.utils import *
import numpy as np
from copy import deepcopy

def flatten(l):
    for i in l:
        yield from i

def flatten_unique(l):
    """ Flattens edge list into vertices and removes multiple references.
        'set()' would be faster, but doesn't preserve order.
    """
    seen = {}
    for i in flatten(l):
        if i not in seen:
            yield i
            seen[i] = True

def make_edges_consecutive(indices, closed=False):
    edges = []
    for i in range(len(indices)-1):
        edges.append((indices[i],indices[i+1]))
    if closed:
        edges.append((indices[i+1],indices[0]))
    return edges

def _faces_to_edges(faces):
    for f in faces:
        if len(f)==2:
            yield f
        else:
            yield from make_edges_consecutive(f, closed=True)
def faces_to_edges(faces):
    seen = {}
    output = []
    for a,b in _faces_to_edges(faces):
        if (a,b) in seen:
            try:
                output.remove((a,b))
            except ValueError:
                pass
            try:
                output.remove((b,a))
            except ValueError:
                pass
        else:
            seen[(a,b)] = True
            seen[(b,a)] = True
            output.append((a,b))
    return output
        
class MeshBuilder(object):
    def __init__(self):
        self.vertices = []
        self.faces = []

    @property
    def current_vertex_index(self):
        return len(self.vertices)

    def add_vertex(self, vertex):
        self.vertices.append(vertex)
        return len(self.vertices)-1
                             
    def add_vertices(self, vertices):
        indices = []
        for v in vertices:
            indices.append(self.add_vertex(v))
        return indices

    def add_face(self, face):
        face = list(face)
        self.faces.append(face)
        return len(self.faces)-1

    def copy_vertices(self, indices):
        old_to_new = dict()
        for i in indices:
            v = self.vertices[i]
            old_to_new[i] = self.add_vertex(v)
        return old_to_new

    def connect_extruded(self, faces, new_map, old_to_new=None):
        edges = list(faces_to_edges(faces))
        indices =(flatten_unique(edges))
        if old_to_new is None:
            old_to_new = dict()
            for i in indices:
                old_to_new[i] = i
        new_faces = []
        for a, b in edges:
            c = new_map[a]
            d = new_map[b]
            f = [old_to_new[a],c,d,old_to_new[b]]
            fi = self.add_face(f)
            new_faces.append(fi)
        return faces 
    def connect_like(self, faces, new_map):
        for f in faces:
            self.faces.append([new_map[i] for i in f])
            
    def connect_loops(self, start_1, start_2, number):
        for i in range(number):
            a = start_1 + i
            b = start_2 + i
            c = start_2 + (i+1) % number
            d = start_1 + (i+1) % number
            self.add_face([a, b, c, d])

    def make_mesh(self, name="Mesh"):
        me = bpy.data.meshes.new("Mesh")
        me.from_pydata([(x,y,z) for x,y,z in self.vertices], [], self.faces)
        me.update()
        return me


def extrude2(path1, path2,width=1):
    """
        Extrudes a single edge of length 'width' along path1 to obtain
        a connected sequence of faces, then extrudes these faces along
        path2 to form a solid body.
    """
    m = MeshBuilder()
    vertices = np.array([[-width/2,0,0],[width/2,0,0]])

    t = next(path1)
    vi = m.add_vertices([t.transform_point(v)[:3] for v in vertices])
    edges = make_edges_consecutive(vi)
    old_to_new = None
    for t in path1:
        new_map = m.copy_vertices(vi)
        for i,j in enumerate(new_map.values()):
            m.vertices[j] = t.transform_point(vertices[vi[i]])[:3]
        m.connect_extruded(edges, new_map, old_to_new)
        old_to_new = new_map

    edges = deepcopy(m.faces)
    vi = list(flatten_unique(edges))
    for t in path2:
        new_map = m.copy_vertices(vi)
        for i in new_map.values():
            m.vertices[i] = t.transform_point(m.vertices[i])[:3]
    m.connect_extruded(edges, new_map)
    m.connect_like(edges,new_map)
    return m.make_mesh()

def pipe(path):
    """ Creates a solid pipe along 'path'. The crosssection is taken from the "vertices" data, which must be
        the same number of vertices at each point of the path.
    """
    m = MeshBuilder()
    t = next(path)
    vertices = list(t.transform(t.data["vertices"]))
    n = len(vertices)
    m.add_vertices(vertices)
    m.add_face(range(n))
    start_1 = 0
    for t in path:
        if n != len(vertices):
            raise ValueError("Number of vertices is not constant.")
        start_2 = m.current_vertex_index
        vertices = list(t.transform(t.data["vertices"]))
        m.add_vertices(vertices)
        m.connect_loops(start_1,start_2, n)
        start_1 = start_2
    m.add_face(reversed(range(m.current_vertex_index-n, m.current_vertex_index)))
    return m.make_mesh()
