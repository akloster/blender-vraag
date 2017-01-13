Vraag
=====
A high level API for Blender, modeled after JQuery
--------------------------------------------------
Blender originated in the Netherlands, and Vraag is Dutch for query, so this is a high level library of utilities for Python scripting in Blender.

Features:
* Vraag Queries: Query and manipulate data objects
* Vraag Array: convert between blender data and numpy arrays
* Vraag Construct: create objects and scenes algorithmically, like in OpenScad
* Vraag Animate: easy setup of animations (not yet implemented)


Vraag Query
-----

For example

```python
	>>> from vraag import V
	>>> V("object")
	V([bpy.data.objects['Camera'], bpy.data.objects['Cube'], bpy.data.objects['Lamp']])
```

This queries all data objects of type "Object". Analogous to CSS' id selectors we can search for an object by its name, and hide it:

```python
	>>> from vraag import V
	>>> V("#Suzanne").hide()
```

Note that Vraag doesn't care in this case what type the object is, it just searches for one with this name.


Vraag Array
-----
Another nice feature is the array accessor, making Blender data easier to use with numpy:

```python
	>>> a = V("object").array.location
	[[ 7.48113155 -6.50763988  5.34366512]
 	[ 0.          0.          0.        ]
 	[ 4.07624531  1.00545394  5.903862  ]]
	>>> V("object").array.location = a + 1
	>>> V("object").array.location
	[[ 8.48113155 -5.50763988  6.34366512]
 	[ 1.          1.          1.        ]
 	[ 5.07624531  2.00545406  6.903862  ]]
```


This API is still mostly undocumented, and rough on all the edges. There are a lot more data structures yet to be covered. The repository is just a preview of what may be possible in the future.

To install Vraag, put the "vraag" directory (the one with the \_\_init\_\_.py, some place where Blender's Python can find it.

Vraag Construct
---------------

Inspired by OpenScad, Vraag Construct offers a way to construct scenes and geometry through code.

Features:
* fully introspectable in Python
* creates native Blender data
    * components can be kept as seperate Objects
    * objects are parented in a hierachy
    * applying the Boolean modifiers is optional
    * materials can be assigned through scripting
    * existing objects can be instantiated
* allows "debugging" the geometry through the Blender interface
* allows easy rigging and animating through usual means

Disadvantages over OpenScad:
* a bit more verbose
* missing some primitives
* no 2D support
* no extrusion/lathe yet

