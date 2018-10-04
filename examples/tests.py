"""
    Vraag Tests

Example command line to run this:
    PYTHONPATH=~/blender-vraag blender playground.blend --background --python-exit-code 1 -P tests.py

"""
import sys
import numpy as np
import bpy
import os
sys.path.append(os.path.dirname(__file__))
from vraag import V
from vraag.utils import find_collections
import unittest


class TestUtils(unittest.TestCase):
    def test_everything(self):
        if bpy.app.version >= (2,80):
            l = list(find_collections("Collection 1"))
            self.assertEqual(len(l),1)
            self.assertEqual(l[0].name, "Collection 1")

class TestInitializations(unittest.TestCase):
    def test_everything(self):
        a = bpy.data.objects["Cube.001"]
        b = bpy.data.objects["Cube"]
        # From objects
        self.assertEqual(V(a)[0], a)
        self.assertEqual(list(V(a,b)), [a,b])


        V.all().scene("Scene.001")
        V.all().scene("Scene", "Scene.001")
        V.all().scene("Scene", "Scene.001").scene("Scene")

        
class TestSelectors(unittest.TestCase):
    def test_queries(self):
        self.assertEqual(V().elements,[])
        self.assertTrue(len(V.all())==len(bpy.data.objects))
        self.assertEqual(V("Cube")[0], bpy.data.objects["Cube"])
        
        self.assertTrue(len(V.basename("Cube"))>1)
        self.assertEqual(len(V.material("Blue")),1)
        
        for vl in (V.material(bpy.data.materials["White"]), V.material("White"), V.material("White", "Blue")):
            pass

        if bpy.app.version >= (2,80):
            vl = V.collection("Collection 1")
        else:
            with self.assertRaises(NotImplementedError):
                V.collection("Collection 1")

class TestVerbs(unittest.TestCase):
    def test_everything(self):
        v = V.all().scene("Scene")
        try:
            v.hide().show()

        except NotImplementedError:
            pass # Ignore for now

class TestConstruct(unittest.TestCase):
    def test_everything(self):
        root = V.construct()
        root.cube()
        
# Kill command line arguments to make unittest.main happier
sys.argv[1:]=[]
unittest.main()
