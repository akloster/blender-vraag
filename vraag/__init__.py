from vraag.query import Selector, VraagList
from vraag.construct import VraagConstruct 
from vraag.utils import up, down, left, right
from vraag.utils import front, back
from vraag.utils import vector
from vraag.construct.text import FontSettings


class BaseV(object):
    def __call__(self, *args):
        if len(args) == 0:
            return VraagList([])
        elif len(args) == 1:
            if isinstance(args[0], str):
                s = Selector(args[0])
                elements = s.token.search()
                return VraagList(elements)
            else:
                return VraagList([args[0]])
        else:
            return VraagList([])
    def construct(self):
        return VraagConstruct()

V = BaseV()

__all__ = ["V",
           "up",
           "down",
           "left",
           "right",
           "front",
           "back",
           "vector",
           "FontSettings"
          ]
