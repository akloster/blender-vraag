import time
import sys
import math
from vraag import *
import bpy


V("Cube").remove()
root = V.construct()

root.stl("koch_flake.stl")
