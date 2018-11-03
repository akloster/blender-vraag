"""
    Contains Query Stuff 
"""
import bpy
import numpy as np
from functools import partial
from vraag.array_access import VraagArrayAccess
from vraag.verbs import verbs

object_prefices = dict(CAMERA='🎥',
                       MESH='📦',
                       LAMP='💡')

class VraagList(object):
    def __init__(self, elements):
        self.elements = list(elements)

    def __getattr__(self, name):
        if name in verbs:
            return partial(verbs[name], self)
        else:
            raise NameError("No Vraag function called '{0}'.".format(name))

    @property
    def array(self):
        self._vraag_array_access = VraagArrayAccess(self)
        return self._vraag_array_access

    @property
    def x(self):
        return np.array([e.location.x for e in self.elements])

    @property
    def y(self):
        return np.array([e.location.y for e in self.elements])

    @property
    def z(self):
        return np.array([e.location.z for e in self.elements])
    def __len__(self):
        return len(self.elements)
    def __iter__(self):
        return iter(self.elements)

    def __getitem__(self, idx):
        if hasattr(idx, "__iter__"):
            idx = list(idx)
            if len(idx) == len(self):
                return self.__class__([e for e,b in zip(self,idx) if b])
        return self.elements[idx]

    def display_names(self):
        for e in self.elements:
            yield object_prefices.get(e.type, '')+ e.name
    def __str__(self):
        return "V({0})".format(", ".join(self.display_names()))
    def __repr__(self):
        return str(self)


