import bpy
from vraag.query import VraagList
from vraag.construct import VraagConstruct 
from vraag.utils import up, down, left, right
from vraag.utils import front, back
from vraag.utils import vector
from vraag.utils import find_collections
from vraag.construct.text import FontSettings
from vraag.node_helpers import NodeTreeHelper

def filter_by_basename(l, arg):
    for o in l:
        if o.name == arg:
            yield o
            continue
        if "." in o.name:
            n = ".".join(o.name.split(".")[:-1])
            if n == arg:
                yield o

class BaseV(object):
    def __call__(self, *args, **kwargs):
        if len(args) == 0:
            return VraagList([])
        
        l = list(self.parse_args(args))
        
        return VraagList(l)

    def parse_args(self, args):
        for arg in args:
            if isinstance(arg, str):
                try:
                    yield bpy.data.objects[arg]
                except KeyError:
                    continue
            if isinstance(arg, bpy.types.Object):
                yield arg
            if isinstance(arg, VraagList):
                yield from arg
            if isinstance(arg, VraagConstruct):
                yield arg.object

    def make_list(self, *args):
        return VraagList(*args)

    def get_all_objects(self):
        for o in bpy.data.objects:
            yield o

    def all(self): 
        return VraagList(self.get_all_objects())

    def basename(self, name):
        elements = filter_by_basename(self.get_all_objects(), name)
        return self.make_list(list(elements)) 

    def material(self, *args):
        return self.all().material(*args)
    def on_layer(self, *args):
        return self.all().on_layer(*args)

    def collection(self, *args):
        if bpy.app.version < (2, 80):
            raise NotImplementedError("Collections are not available in Blender versions before 2.80.")

        elements = list()
        for collection in find_collections(*args):
            elements += collection.objects
        return self.make_list(list(elements))


    def construct(self):
        return VraagConstruct()


V = BaseV()

__all__ = ["V",
           "up",
           "down",
           "left",
           "right",
           "front",
           "back",
           "vector",
           "FontSettings",
           "NodeTreeHelper"
          ]
