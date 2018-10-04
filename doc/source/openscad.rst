OpenSCAD integration
====================

OpenSCAD is an Open Source language and "compiler" to compose 3D objects through constructive solid geometry. It is very popular in the RepRap community and is at the heart of Thingiverse customizers. OpenSCAD also served as an inspiration for Vraag Construct.

This module allows you to use OpenSCAD scripts from Python inside Blender. It also caches the resulting according to hashes derived from the code used to generate them.

.. code-block:: python

    from vraag.openscad import OpenScadEnvironment

    environment = OpenScadEnvironment(binary="/home/andi/openscad/openscad")
    mesh = environment.run_string("cube([2,3,4]);")

    V.construct().mesh(mesh)

The way this works is to create an OpenScadEnvironment instance. It serves as a template for an environment to run OpenSCAD code in. Unfortunately, OpenSCAD is not a particularly well behaved command line tool. For example it doesn't read code from stdin, doesn't stream output to stdout and doesn't offer a way to add library directories.

To work around these points, OpenSCAD is run inside a temporary directory created for each run. All the necessary code is copied there (which isn't much, usually) and the exported STL file is fetched from there.

To get around the problems with the library paths, you can specify requirements in the environment, which are then copied to the temporary path. You can then distribute the OpenSCAD library together with your script. The library is also hashed, so if you modify it, the environment knows to recompile the mesh.
