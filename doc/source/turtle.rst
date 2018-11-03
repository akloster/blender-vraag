Turtle System
======================

"Turtle graphics" was originally invented for the Logo programming language, which was created to teach basic programming. It was a system to move a robot, a real or simulated one, to draw figures on a screen or a sheet of paper. It would have instructions like "go forward", "turn left" and so on.

This implementation works in 3D, and the basic output is a sequence of transformation matrices. These can then be used to place objects in the scene (with location, orientation and scale), create points in a mesh, create points in a path or a myriad of other things.

For mesh modeling there is the mesh builder framework. Here you can use one or more turtle paths to define meshes. This way of algorithmic modeling often produces "saner" results than the CSG approach which work better as a base stock for manual editing or further CSG.

.. code-block:: python

    def rounded_box():
        t = TurtlePoint()
        for i in range(4):
            yield from t.move(forward, 2)
            yield from t.turn(up, 90, 8)

This function is a generator and will yield 40 different TurtlePoints (4*(2+8)).


.. code-block:: python
    for t in rounded_box():
        print(t.transform_point((0,0,0)))

This prints out 40 vectors which trace a rounded rectangle.

.. code-block:: python
    for t in rounded_box():
        print(t.transform_point((0,0,0))) 

