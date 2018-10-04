import sys
import numpy as np
import bpy
import os
sys.path.append(os.path.dirname(__file__))
from vraag import V
import unittest


class TestSelectors(unittest.TestCase):
    def test_queries(self):
        print("hello")

class TestVerbs(unittest.TestCase):
    def test_everything(self):
        print("hello")

# Kill command line arguments to make unittest.main happier
sys.argv[1:]=[]
unittest.main()
sys.exit()
