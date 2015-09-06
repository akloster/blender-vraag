import bpy
import numpy as np


class VraagArrayAccess(object):
    def __init__(self, vraag_list):
        self.vraag_list = vraag_list

    def _as_array(self, property_name, m, dtype=np.float32):
        n = len(self.vraag_list)
        a = np.zeros((n, m), dtype=dtype)
        for i, o in enumerate(self.vraag_list):
            a[i,:] = getattr(o, property_name)
        return a

    def _shape_error(self, expected, gotten):
        return ValueError("Expected array of shape %s, got shape %s" \
                            % (expected, gotten))
    def _set_from_array(self, property_name, a, m, dtype=np.float32):
        n = len(self.vraag_list)
        if a.shape != (n,m):
            raise self._shape_error([n,m], a.shape)

        for i, o in enumerate(self.vraag_list):
            o.location = a[i,:]
        return self.vraag_list

    @property
    def location(self):
        return self._as_array("location", 3)

    @location.setter
    def location(self, a):
        self._set_from_array("location", a, 3) 

    @property
    def scale(self):
        return self._as_array("scale", 3)

    @property
    def rotation_euler(self):
        return self._as_array("rotation_euler", 3)

    @property
    def rotation_quaternion(self):
        return self._as_array("quaternion", 4)

