import bpy
import numpy as np
from functools import partial
from vraag.array_access import VraagArrayAccess
from vraag.verbs import verbs

id_name_legal_chars = set([c for c in "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
            "abcdefghijklmnopqrstuvxyz"
            "1234567890._"])


class Token(object):
    def __init__(self, query_string=""):
        self.child = None
        self.siblings = []
        self.query_string = query_string
    def add(self, token, mode): 
        if mode in ["begin", "descendant"]:
            if self.child is None:
                self.child = token
            else:
                self.child.add(token, mode)
        else:
            if self.child is None:
                self.siblings.append(token)
            else:
                self.child.add(token, mode)
    def __str__(self):
        s = self.__class__.__name__
        s += " %s " % repr(self.query_string)
        s +="("
        if self.siblings:
            s += ( ",".join(["%s"%o for o in self.siblings]))
        if self.child is not None:
            s += "-->%s" % self.child
        s += ")"
        return s
    def build_list(self):
        """ Builds a list from just the query_string. Used for the first token."""
        return []


def find_children(elements):
    visited = {}
    new_elements = []
    def add(element):
        addr = element.as_pointer()
        if not addr in visited:
            new_elements.append(element)
            visited[addr] = True
            search(element)

    def search(element):
        rna = element.rna_type.name
        if rna == "Scene":
            for o in element.objects:
                add(o)
        if rna == "Object":
            add(element.data)
    for element in elements:
        search(element)
    return new_elements

class RootToken(Token):
    def search(self):
        elements = self.child.build_list()
        base = self.child
        while 1:
            for token in base.siblings:
                elements = token.filter(elements)
            if base.child is None:
                break
            else:
                elements = find_children(elements)
            base = base.child
            elements = base.filter(elements)
        return elements


class TypeToken(Token):
    types = {"object": "objects",
             "objects": "objects",
             "scene": "scenes",
             "scene": "scenes",
             "camera": "cameras",
             "cameras": "cameras",
             "lamp": "lamps",
             "lamps": "lamps",
             "material": "materials",
             "materials": "materials"}

    def build_list(self):
        l = []
        q = self.query_string.lower()
        if q in self.types:
            attribute = self.types[q]
            for o in getattr(bpy.data, attribute):
                l.append(o)
        return l


    def filter(self, elements):
        new_elements = []
        q = self.query_string.lower()
        for element in elements:
            if (element.rna_type.name).lower() == q:
                new_elements.append(element)
        return new_elements


class NameToken(Token):
    collections = ["objects", "actions", "scenes", "materials"]
    def build_list(self):
        elements = []
        for c in self.collections:
            collection = getattr(bpy.data, c)
            if self.query_string in collection:
                elements.append(collection[self.query_string])
        return elements



    def filter(self, elements):
        new_elements = []
        for element in elements:
            if hasattr(element, "name"):
                if element.name == self.query_string:
                    new_elements.append(element)
        return new_elements


class ContextToken(Token):
    """ Search and filter by context """
    context_single_items = ["scene", "active_object", "window", "area"]
    def build_list(self):
        elements = []
        if self.query_string in self.context_single_items:
            item = getattr(bpy.context, self.query_string)
            elements.append(item)
        return elements
    def filter(self):
        return []

class VraagList(object):
    def __init__(self, elements):
        self.elements = elements
    def __getattr__(self, name):
        if name in verbs:
            print(self)
            return partial(verbs[name], self)
        else:
            raise NameError("No Vraag function called '{0}'.".format(name))

    @property
    def array(self):
        self._vraag_array_access = VraagArrayAccess(self)
        return self._vraag_array_access

    def __len__(self):
        return len(self.elements)
    def __iter__(self):
        return iter(self.elements)


    def __getitem__(self, i):
        return self.elements[i]


    def __str__(self):
        return "V({0})".format(self.elements)
    def __repr__(self):
        return str(self)

class Selector(object):
    def __init__(self, query):
        self.query = query
        self.token = RootToken()
        self.tokenize(query)

    def parse(self):
        def white_space():
            c = " "
            while c==" " :
                c = yield
            return c
        def id_name():
            name = ""
            c = yield
            while c in id_name_legal_chars:
                name += c
                c = yield
            yield 1
            return name

        mode = "begin"
        c = yield from white_space()
        while 1:
            if mode is "descendant" and c==" ":
                c = yield from white_space()
            if c == "\n":
                break
            if c == "#":
                name = yield from id_name()
                self.token.add(NameToken(name), mode)
            elif c == "§":
                group_name = yield from id_name()
                print("By Group:", group_name)
            elif c == "@":
                name = yield from id_name()
                self.token.add(ContextToken(name), mode)
            else:
                name = c + (yield from id_name())
                self.token.add(TypeToken(name), mode)
            c = yield
            if c in "#§@":
                mode = "attach"
            else:
                mode = "descendant"

    def tokenize(self, query):
        tokenizer = self.parse()
        next(tokenizer)
        pos = 0
        while 1:
            if pos < len(query):
                # Send current character
                c = query[pos]
            else:
                # Send end of line
                c = "\n"

            try:
                backsteps = tokenizer.send(c)
            except StopIteration:
                break

            # Handle backstepping
            if backsteps is not None:
                pos -= backsteps
            else:
                pos += 1

def V(query_string):
    s = Selector(query_string)
    elements = s.token.search()
    return VraagList(elements)

