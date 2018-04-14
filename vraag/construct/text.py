import numpy as np
import math
import bpy
from vraag.utils import *
from .base import VraagConstruct, register_constructor
from .primitives import VraagObject
from copy import copy


class FontSettings(object):
    DEFAULT_SETTINGS = dict(align_x="LEFT",
                            align_y="TOP_BASELINE",
                            bevel_depth=0.0,
                            extrude = 0,
                            font = None,
                            follow_curve=None,
                            font_bold=None,
                            font_bold_italic=None,
                            font_italic=None,
                            offset_x=0,
                            offset_y=0,
                            shear=0,
                            size=1,
                            small_caps_scale=0.75,
                            space_character=1,
                            space_line=1,
                            space_word=1,
                            underline_height=0,
                            use_fast_edit=False
                           )
    def __init__(self, **kwargs):
        self.settings = copy(self.DEFAULT_SETTINGS)
        self.settings.update(**kwargs)

    def update(self, **kwargs):
        args = copy(self.settings)
        args.update(**kwargs)
        return self.__class__(**args)

class Font(VraagObject):
    def __init__(self, parent, text="", name="Cube", settings=None):
        super().__init__(parent, name)
        self.text = text
        self.settings = settings
        self.object = self.build()

    def build(self):
        font_curve = bpy.data.curves.new(type="FONT",name="myFontCurve")
        if self.settings:
            for key, value in self.settings.settings.items():
                if key is "font" and value is None:
                    continue
                setattr(font_curve, key, value)
        font_curve.body = self.text
        ob = bpy.data.objects.new(self.name, font_curve)
        self.setup(ob)
        return ob


register_constructor(Font, "font")
