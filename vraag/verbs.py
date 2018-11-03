import bpy
import bpy_types
from functools import wraps
import io_mesh_stl.blender_utils
import io_mesh_stl.stl_utils
from vraag.utils import find_materials

verbs = {}
def vraag_verb(method_or_name, base=True, extended=True):
    def decorator(method):
        verbs[method_or_name] = method

        return method
    if callable(method_or_name):
        verbs[method_or_name.__name__] = method_or_name
        return method_or_name
    else:
        return decorator

def find_materials(*args):
    for arg in args:
        if isinstance(arg, str):
            yield bpy.data.materials[arg]
            continue
        if isinstance(arg, bpy.types.Material):
            yield arg
            continue

        try:
            yield from find_materials(list(arg))
        except TypeError as te:
            pass

def filter_by_materials(elements, *args):
    materials = list(find_materials(*args))
    for o in elements:
        for ms in o.material_slots:
            if ms.material in materials:
                yield o
                break


@vraag_verb
def on_layer(vl, number):
    return vl.__class__([element for element in vl if element.layers[number]])

@vraag_verb
def material(vl, *args):
    return vl.__class__(list(filter_by_materials(vl.elements, *args)))


def find_scenes(*args):
    for arg in args:
        if isinstance(arg, str):
            yield bpy.data.scenes[arg]
            continue
        if isinstance(arg, bpy.types.Scene):
            yield arg
            continue
        try:
            l = list(args)
        except TypeError as te:
            pass
        else:
            yield from find_scenes(l)


def filter_by_scenes(elements, *args):
    scenes = list(find_scenes(*args))
    for o in elements:
        for scene in scenes:
            if o.name in scene.objects:
                yield o
                break

@vraag_verb
def scene(vl, *args):
    return vl.__class__(list(filter_by_scenes(vl.elements, *args)))

@vraag_verb
def hide(vl):
    if bpy.app.version >= (2,80):
        raise NotImplementedError("Hide is not yet implemented for Blender 2.80 and above.")

    for element in vl.elements:
        element.hide = True
    return vl


@vraag_verb
def names(vl):
    for element in vl.elements:
        yield element.name


@vraag_verb
def show(vl):
    for element in vl.elements:
        try:
            element.hide = False
        except:
            continue
    return vl.__class__(vl.elements)

@vraag_verb
def set_prop(vl, property_name, value):
    for element in vl.elements:
        try:
            setattr(element, property_name, value)
        except:
            continue
    return vl


@vraag_verb
def get_prop(vl, property_name):
    l = []
    for element in vl.elements:
        try:
            l.append(getattr(element, property_name))
        except:
            continue
    return l

@vraag_verb
def iget_prop(vl, property_name):
    for element in vl.elements:
        try:
            yield getattr(element, property_name)
        except:
            continue

@vraag_verb
def iprop(vl, property_name, value=None):
    l = []
    if value is None:
        yield iget_prop(vl, property_name)
    else:
        yield iset_prop(vl, property_name, value)

@vraag_verb
def prop(vl, property_name, value=None):
    l = []
    if value is None:
        return get_prop(vl, property_name)
    else:
        return set_prop(vl, property_name, value)

@vraag_verb("apply")
def vraag_apply(vl, func):
    for element in vl.elements:
        yield func(element)
    return vl

@vraag_verb("map")
def vraag_map(vl, func):
    return map(func, vl.elements)

@vraag_verb("filter")
def vraag_filter(vl, func):
    return vl[vl.map(func)]

@vraag_verb
def activate(vl):
    activation_types = [(bpy_types.Object, bpy.context.scene.objects)]
    for activation_type, collection in activation_types:
        for element in vl.elements:
            if type(element) is activation_type:
                collection.active = element
                break
    return vl

@vraag_verb
def select(vl):
    for element in vl.elements:
        if type(element) is bpy_types.Object:
            element.select = True
    return vl

@vraag_verb
def remove(vl):
    for element in vl.elements:
        bpy.data.objects.remove(element, do_unlink=True)
    return None

@vraag_verb
def deselect(vl):
    for element in vl.elements:
        element.select = False
    return vl

@vraag_verb
def export_stl(vl, filepath, ascii=False):
    faces = []
    for element in vl.elements:
        faces += list(io_mesh_stl.blender_utils.faces_from_mesh(element,
                            use_mesh_modifiers=True,
                            global_matrix=element.matrix_world
                            ))
    io_mesh_stl.stl_utils.write_stl(filepath, faces, ascii=ascii)
    return vl
