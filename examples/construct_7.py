import time
import sys
import math
from vraag import *
import bpy


V("Cube").remove()
root = V.construct()


root.prism([[0,1],
              [1.5,1.5],
              [1,0],
              [1.5,-1.5],
              [0,-1],
              [-1.5,-1.5],
              [-1,0],
              [-1.5,1.5],
             ])
