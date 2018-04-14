import time
import sys
import math
from vraag import *
import bpy


V("#Cube").remove()
root = V.construct()


inconsolata_regular=bpy.data.fonts.load("Inconsolata-Regular.ttf")
font = FontSettings(font=inconsolata_regular)
heading_font = font.update(align_x="CENTER", extrude=0.1)
paragraph_font =font.update(size=0.25)


root.translate((0,4,0)).font(text="Hello", settings=heading_font)
root.translate((-5,3,0)).font(text="Lorem ipsum dolor sit amet, consectetur adipiscing elit", settings=paragraph_font)
