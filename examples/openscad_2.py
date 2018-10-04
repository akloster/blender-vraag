from vraag import *
from vraag.openscad import OpenScadEnvironment, OpenScadRun
import os

class MyEnvironment(OpenScadEnvironment):
    requirements = [("simple_lib.scad", "simple_lib.scad")]
V("Cube").remove()
environment = MyEnvironment(binary="/home/andi/openscad/openscad",
                            cache_dir=os.path.join(os.getcwd(),".osc-cache"))

def house(roof):
    mesh = environment.run_string("""use <simple_lib.scad>;\n house("{roof}");""".format(roof=roof))
    return mesh

root = V.construct()

root.translate(left*1).mesh(house("pitched"))
root.translate(right*1).mesh(house("domical"))

