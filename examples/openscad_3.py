from vraag import *
from vraag.openscad import OpenScadEnvironment, OpenScadRun
import os

V("Cube").remove()
cache_dir = os.path.join(os.getcwd(), ".osc-cache")
environment = OpenScadEnvironment(binary="/home/andi/openscad/openscad",
                                  cache_dir=cache_dir)

def gear(number_of_teeth = 20, circular_pitch=200, rim_thickness=8, circles=4):
    code = """
            use <MCAD/involute_gears.scad>;
            gear(number_of_teeth={0},
                 circular_pitch={1},
                 rim_thickness={2},
                 circles={3});
                                  """.format(number_of_teeth, circular_pitch,
                                            rim_thickness, circles)
    mesh = environment.run_string(code)
    return mesh

root = V.construct()


gears = (
    dict(number_of_teeth=15, circular_pitch=200),
    dict(number_of_teeth=25, circular_pitch=200),
    dict(number_of_teeth=30, circular_pitch=200),
    dict(number_of_teeth=40, circular_pitch=200),

    dict(number_of_teeth=15, circular_pitch=200, rim_thickness=5),
    dict(number_of_teeth=25, circular_pitch=200, rim_thickness=5),
    dict(number_of_teeth=30, circular_pitch=200, rim_thickness=5),
    dict(number_of_teeth=40, circular_pitch=200, rim_thickness=5),
)

for i,gear_params in enumerate(gears):
    root.translate((i%4)*50, (i//4)*50, 0).mesh(gear(**gear_params))

