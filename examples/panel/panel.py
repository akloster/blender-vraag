import numpy as np
import math
from vraag import *
import bpy


# common fudge factor for making blender's CSG behave
e = 0.0001

# Setup scenes
preview_scene = bpy.data.scenes[0]
export_scene_panel = bpy.data.scenes.new("Panel Export")
export_scene_mask = bpy.data.scenes.new("Mask Export")
# Boolean modifiers/operators only work reliably when the objects are in the current scene
bpy.context.screen.scene = preview_scene
root = V.construct().scene(preview_scene)

# Link the Slider from a library
with bpy.data.libraries.load("//switch.blend", relative=True, link=True) as (data_from, data_to):
        data_to.meshes = ["Switch"]

switch_mesh = bpy.data.meshes['Switch']
switch_material = bpy.data.materials['SwitchMaterial']

# Link the Switch from a library
with bpy.data.libraries.load("//slider.blend", relative=True, link=True) as (data_from, data_to):
        data_to.meshes = ["Slider"]

slider_mesh = bpy.data.meshes["Slider"]

panel_material = bpy.data.materials['PanelMaterial']


spacing = 20
tolerance = 0.5
screw_margin = 5
screw_diameter = 3

# x,y, "text"
switches = [
            (spacing*0, 0, "A"),
            (spacing*1, 0, "B"),
            (spacing*2, 0, "C"),
            (spacing*3, 0, "D"),
           ]

slider_y = -55
sliders = [
            (spacing*0, slider_y),
            (spacing*1, slider_y),
            (spacing*2, slider_y),
            (spacing*3, slider_y)
           ]

gunplay_rg=bpy.data.fonts.load("gunplay rg.ttf")
font = FontSettings(font=gunplay_rg, size=15, align_x="CENTER", offset=-0.3)
cut_font = font.update(extrude=5)

panel_width = 100
panel_height = 120
panel = root.material(panel_material).box((-panel_width/2, panel_height/2, 0),
                                          (panel_width/2, -panel_height/2, -2.5))

mask = V.construct().scene(export_scene_mask)
mask_base = mask.box((-panel_width/2, panel_height/2,0),(panel_width/2, -panel_height/2, -0.8))

x = panel_width/2-screw_margin
y = panel_height/2-screw_margin

screws = [(-x,y),
          (x,y),
          (x,-y),
          (-x,-y)
         ]
for x,y in screws:
    cylinder = root.translate((x,y,0))\
                   .cylinder(radius=screw_diameter/2+tolerance,
                               height=10)
    panel.difference(cylinder, apply_modifier=True, keep=False)

fixture_pos = (-30,45,-0.1)
fixtures = root.translate(fixture_pos).material(switch_material)

for x,y,text in switches:
    bpy.context.screen.scene = preview_scene
    fixtures.translate((x,y,0))\
            .mesh(switch_mesh, name="Switch.000")\
            .translate((0,-15,0.65)).font(text, settings=font)
    f = root.font(text, settings=cut_font)
    f_mesh = f.object.to_mesh(scene=export_scene_mask, apply_modifiers=True,
                                    settings='RENDER')
    cutout = mask.translate(fixture_pos).translate((x,y,0)).translate((0,-15,1)).mesh(f_mesh)
    panel.union(fixtures.translate((x,y-7.3,0)).box((-5,-3.3,0),(5,-1.5,-15)))
    hole = fixtures.translate((x,y,0)).cylinder(radius=3.4, height=20)
    panel.difference(hole)
    bpy.context.screen.scene = export_scene_mask
    mask_base.difference(cutout)
    V(f.object).remove()

bpy.context.screen.scene = preview_scene
# Box walls
wall_width = 0.4*4
box_height = 50
walls = root.translate(down*2.5).material(panel_material)
a = panel_width/2
b = panel_height/2 
panel_walls = walls.box((-a,-b,-box_height),(a, b, 0))

a = panel_width/2-wall_width 
b = panel_height/2-wall_width
c = screw_margin*2.8

points = [(-a+c,-b),
          (a-c,-b),
          (a,-b+c),
          (a,b-c),
          (a-c,b),
          (-a+c,b),
          (-a, b-c),
          (-a, -b+c)
         ]

a = panel_width/2-screw_margin
b = panel_height/2-screw_margin
inner_walls = walls.prism(points, height=(10,-box_height-10))
panel_walls.difference(inner_walls)

for (x,y) in [(-a,-b),(a,b),(-a,b),(a,-b)]:
    cyl = panel_walls.difference(walls.translate((x,y,0)).cylinder(radius=3.1, height=(0,-10)))
    panel_walls.difference(cyl)


wedge = walls.translate(down*30).rotate(right,5).box((-2*a, -2*a, -100),(2*a, 2*a,0))
panel_walls.difference(wedge)

V(panel_walls.object).export_stl("box_wall.stl")
bpy.context.screen.scene = preview_scene

def tick_objects(pos):
    offset = -44.2+15
    ticks = np.linspace(offset, offset+60,11)
    tick_d = 5
    h = 2
    yield pos.translate((0,ticks[0],0)).cube((15,h, tick_d))
    yield pos.translate((0,ticks[-1],0)).cube((15,h, tick_d))
    yield pos.translate((0,ticks[5],0)).cube((15,h, tick_d))

    for i,p in enumerate(ticks):
        yield pos.translate((0, p,-2)).cube((10, h-0.0001, tick_d))


for x,y in sliders:
    bpy.context.screen.scene = preview_scene
    pos = fixtures.translate((x,y,0))
    #pos.mesh(slider_mesh, name="Slider.000")
    bottom_hold = pos.translate((0,-44.2,0))
    panel.union(bottom_hold.box((-5, 0, 0),(5, -2, -15)))
    panel.union(
        bottom_hold.box((5-e, 6, -7.5), (-5+e, 0+e, -1.5)),
        pos.box((5-e, +37, -7.5), (-5+e, 44, -1.5))
    )

    hole = fixtures.translate((x,y,0)).cube(size=(3.1,72,10))
    panel.difference(hole)

    bpy.context.screen.scene = export_scene_mask
    mask_base.difference(*(tick_objects(mask.translate(fixture_pos).translate((x,y,0)))))



ep = V.construct().scene(export_scene_panel).rotate(right,180)
export_panel = ep.mesh(panel.object.data.copy())


# I wasn't able to get a perfect surface with my printer, mainly because some of the contours
# in the first layer always got messed up, or there was material where it shouldn't, resulting
# in bumps etc.
# So I added a sort of pseudo raft which eliminates any of the tricky contours. Now I
# have to cut out the holes with a scalpel, but it looks much better!

bpy.context.screen.scene = export_scene_panel
export_panel.union(ep.box((-panel_width/2, panel_height/2, 0+e),
                                          (panel_width/2, -panel_height/2, -0.2)))


bpy.context.screen.scene = preview_scene
V(mask_base.object).hide()
