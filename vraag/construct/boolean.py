import numpy as np
import math
import bpy
from vraag.utils import *

from .base import VraagConstruct, register_constructor

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

register_constructor(Union, "union")
class Difference(VraagBoolean):
    operation = "DIFFERENCE"

register_constructor(Difference, "difference")
class Intersection(VraagBoolean):
    operation = "INTERSECTION"

register_constructor(Intersection, "intersection")
