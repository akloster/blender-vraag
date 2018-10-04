"""
    Contains Query Stuff 
"""
import bpy
import numpy as np
from functools import partial
from vraag.array_access import VraagArrayAccess
from vraag.verbs import verbs



class VraagList(object):
    def __init__(self, elements):
        self.elements = elements

    def __getattr__(self, name):
        if name in verbs:
            return partial(verbs[name], self)
        else:
            raise NameError("No Vraag function called '{0}'.".format(name))

    @property
    def array(self):
        self._vraag_array_access = VraagArrayAccess(self)
        return self._vraag_array_access

    def __len__(self):
        return len(self.elements)
    def __iter__(self):
        return iter(self.elements)


    def __getitem__(self, i):
        return self.elements[i]


    def __str__(self):
        return "V({0})".format(list(self.names()))
    def __repr__(self):
        return str(self)



def V(*args, **kwargs):
    if len(args) == 0:
        return VraagList([])
    elif len(args) == 1:
        if isinstance(args[0], str):
            s = Selector(args[0])
            elements = s.token.search()
            return VraagList(elements)
        else:
            return VraagList([args[0]])
    else:
        return VraagList([])

