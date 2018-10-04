from vraag import *
from vraag.openscad import OpenScadEnvironment, OpenScadRun

V("Cube").remove()
environment = OpenScadEnvironment(binary="/home/andi/openscad/openscad")

mesh = environment.run_string("cube([2,3,4]);")

V.construct().mesh(mesh)

