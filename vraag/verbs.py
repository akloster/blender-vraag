import bpy
import bpy_types
from functools import wraps

verbs = {}
def vraag_verb(method_or_name):
    def decorator(method):
        verbs[method_or_name] = method

        return method
    if callable(method_or_name):
        verbs[method_or_name.__name__] = method_or_name
        return method_or_name
    else:
        return decorator

@vraag_verb
def hide(vl):
    for element in vl.elements:
        try:
            element.hide = True
        except:
            continue

@vraag_verb
def show(vl):
    for element in vl.elements:
        try:
            element.hide = False
        except:
            continue

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
        yield iget_prop(vl.elements, property_name)
    else:
        yield iset_prop(vl.elements, property_name, value)

@vraag_verb
def prop(vl, property_name, value=None):
    l = []
    if value is None:
        return get_prop(vl.elements, property_name)
    else:
        return set_prop(vl.elements, property_name, value)

@vraag_verb("apply")
def vraag_apply(vl, func):
    for element in vl.elements:
        yield func(element)
    return vl

@vraag_verb("map")
def vraag_map(vl, func):
    return map(func, vl.elements)

@vraag_verb
def activate(vl):
    activation_types = [(bpy_types.Object, bpy.context.scene.objects)]
    for activation_type, collection in activation_types:
        for element in vl.elements:
            if type(element) is activation_type:
                collection.active = element
                break

@vraag_verb
def select(vl):
    for element in vl.elements:
        if type(element) is bpy_types.Object:
            element.select = True

@vraag_verb("remove")
def remove(vl):
    for element in vl.elements:
        bpy.data.objects.remove(element, do_unlink=True)
    return None

@vraag_verb
def deselect(vl):
    for element in vl.elements:
        element.select = False
