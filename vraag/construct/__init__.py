import numpy as np
import math
import bpy
from vraag.utils import *

from .base import VraagConstruct, register_constructor
from .primitives import VraagObject
from .transform import *
from .boolean import *
from .turtle import *
from .mesh_builder import MeshBuilder, extrude2


class Material(VraagObject):
    def __init__(self, parent, material):
        super().__init__(parent)
        self._material = material

register_constructor(Material, "material")

class Scene(VraagObject):
    def __init__(self, parent, scene):
        super().__init__(parent)
        _scene = None
        if hasattr(scene, 'rna_type'):
            if scene.rna_type.name == 'Scene':
                _scene = scene
        if not _scene:
            _scene = bpy.data.scenes[scene]
        self._scene = _scene

register_constructor(Scene, "scene")

class Layers(VraagObject):
    def __init__(self, parent, *layers):
        super().__init__(parent)
        _layers = None
        self._layers = layers

register_constructor(Layers, "layers")
