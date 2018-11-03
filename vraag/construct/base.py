import types
import numpy as np
import math
import bpy
from vraag.utils import *



constructors = {}

def register_constructor(cls, name):
    constructors[name] = cls

class ConstructorMeta(type):
    def __init__(cls, name, bases, namespace):
        super(ConstructorMeta, cls).__init__(name, bases, namespace)


class ConstructorAttribute(object):
    def __init__(self, parent, constructor):
        self.constructor = constructor 
        self.parent = parent

    def __call__(self, *args, **kwargs):
        obj = self.constructor(self.parent, *args, **kwargs)
        self.parent.add_child(obj)
        return obj


class VraagConstruct(object, metaclass=ConstructorMeta):
    """ Baseclass for all construction nodes."""

    constructors = {}
    def __init__(self, parent=None):
        self.parent = parent
        self.children = []
        self.matrix = identity()
        self.object = None
        for name, constructor in constructors.items():
            if not hasattr(self, name):
                caller = ConstructorAttribute(self, constructor)
                setattr(self, name, caller)


    def add_child(self, obj):
        self.children.append(obj)


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

    def build(self):
        return None

    def get_parent_object(self):
        p = self.parent
        while p.parent:
            if p.object:
                return p.object
            p = p.parent

    def get_last_material_node(self):
        node = self.parent

        while node:
            if hasattr(node, "_material"):
                return node
            node = node.parent

        return None


    def get_last_scene_node(self):
        node = self.parent

        while node:
            if hasattr(node, "_scene"):
                return node
            node = node.parent

        return None


    def get_last_layers_node(self):
        node = self.parent

        while node:
            if hasattr(node, "_layers"):
                return node
            node = node.parent

        return None
    def clean(self):
        if self.object:
            bpy.data.objects.remove(self.object, do_unlink=True)
        for child in self.children:
            child.clean()
        self.children = []
        return self




