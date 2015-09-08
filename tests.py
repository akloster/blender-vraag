import sys
import numpy as np
import bpy
import os
sys.path.append(os.path.dirname(__file__))
from vraag import V
import unittest


class TestSelectors(unittest.TestCase):
    def test_queries(self):
        test_queries = ["object",
                        "objects",
                        "object#Cube",
                        "#Cube",
                        "@scene object",
                        "@scene camera",
                        "#Scene1 object#Suzanne"
                        "camera",
                        "lamp"
                        ]

        for q in test_queries:
            V(q)

class TestArrays(unittest.TestCase):
    def test_array(self):
        V("objects").array.location
        V("objects").array.scale
        V("objects").array.rotation_euler

    def test_array2(self):
        a =  V("objects").array.location
        V("objects").array.location = a+1
        V("objects").array.location
        with self.assertRaises(ValueError):
            V("objects").array.location = np.array([[0,1,2,3,4],[2,4,6,8]])

class TestVerbs(unittest.TestCase):
    def test_everything(self):
        list(V("object").map(lambda o: o.location))

        V("object").hide()
        V("object").show()
        suzanne = V("#Suzanne")[0]
        V("#Suzanne").activate()
        self.assertEqual(suzanne, bpy.context.scene.objects.active)


sys.argv[1:]=[]
unittest.main()
