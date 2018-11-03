Query API
======================

When scripting Blender, one of the more common tasks is to find objects with certain properties and do stuff to them. Vraag provides a way to query and filter Blender objects and operate on them.


Introduction
---------------

.. code-block:: python

    V.all()

Returns a VraagList with all objects in the current file.

.. code-block:: python

    V("Suzanne")

Returns a List with one object called Suzanne.

.. code-block:: python

    V.basename("Cube")

Will match all objects whose basename is "Cube", for example "Cube.001" and "Cube.002".

.. code-block:: python

    V.scene("Opening Scene")

Returns all objects in "Opening Scene".


.. code-block:: python

    vl = V.basename("Cube")

    vl.hide()
    vl.show()

First hides then shows all Objects named "Cube" or "Cube.*".

.. code-block:: python

    vl = V.basename("Cube")
    vl.save_stl("Cube.stl")

This API is still very incomplete. Any feature suggestions or pull requests welcome!
