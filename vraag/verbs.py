import bpy

verbs = {}
def vraag_verb(f):
    def wrapped(*args, **kwargs):
        return f(*args, **kwargs)
    verbs[f.__name__] = f
    return wrapped

@vraag_verb
def hide(vl):
    for element in vl.elements:
        try:
            element.hide = True
        except:
            continue

@vraag_verb
def show(vl):
    for element in elements:
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

@vraag_verb
def apply(vl, func):
    for element in vl.elements:
        yield func(element)
    return vl

@vraag_verb
def map(vl, func):
    return apply(vl.elements, func)
