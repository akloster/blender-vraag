Vraag Construct
==================

Vraag Construct is a library and paradigm to compose Blender scenes programatically. It is largely inspired by OpenSCAD, but uses Blender's facilities to create and modify objects.


Basics
------
Typically you create a root node.


.. code-block:: python

    root = V.construct()
    V.sphere()

This creates a sphere with radius 1 at <0,0,0>.

Construct Nodes do not always represent Blender objects, but most of the time they represent a transformation.


.. code-block:: python

    V.translate((1,0,0)).sphere()

Creates a sphere which is translated one unit to the right.

Many functions take numpy arrays as inputs, which means you can also do this:

.. code-block:: python

    V.translate(right*3).sphere()

Where right is a name imported from Vraag, representing a numpy array. There are also left, up, down, front and back.

Boolean Operations
-------------------

.. code-block:: python

    root.cube().difference(root.sphere())

This subtracts a Sphere from a Cube. The sphere is subsequently deleted.

.. code-block:: python

    root.cube().difference(root.sphere(), keep=True)

The "keep" parameter determines whether or not to keep the passed object.

.. code-block:: python

    root.cube().difference(root.sphere(), apply_modifier=False)

The default, "apply_modifier=True" means that the Boolean modifier is applied (and deleted). With this option set to True, the Boolean operator is kept in place, and it can then be inspected and modified by the user later.

In addition to "difference" there are also "union" and "intersect", working in accordance with Blender's Boolean modifier.


Primitives
-----------

Construct implements several primitive shapes.

.. py:method:: cube(size=(1,1,1))

    Basic Cube with a size, centered at <0,0,0>.

box

sphere
cylinder

plane

prism

mesh

Instantiates a mesh, from either a Mesh object, an object, or from a library.

stl

The "stl" method loads an STL file as a mesh. Especially for bigger meshes, loading models from other Blend files is much faster than importing them as an STL file. It often makes sense to load STL files into a blender library once and then reusing the Blender data objects.


