Installation and using
========================


Shallow integration with Blender Python
-----------------------------------------
Unfortunately Blender does not have any default package management, which means it can be a pain to distribute slightly more complicated addons. Vraag therefore does not require external dependencies.

However, the vraag library is imported as a directory, thus the "vraag" folder must be in the PYTHONPATH. This can be accomplished by copying/linking it into blender's site-packages directory, or by adding the blender-vraag directory to the PYTHONPATH environment variable.

Currently, the Vraag library is solely developed under Linux, but it doesn't contain anything which should be impossible to run on Windows. Any suggestions, bug reports etc are welcome.

So far, Vraag does not support Blender 2.8. A lot has changed in the way to handle objects and scenes, so parts of the library may need a rethink.

One way to run examples or scripts is the following commandline:

PYTHONPATH=~/blender-vraag blender myfile.blend -P myscript.py


PIP
-----------------------------------------------

This has only been tested for Blender 2.79b on Ubuntu. It may or may not work for other systems.

.. code-block:: bash
    wget https://bootstrap.pypa.io/get-pip.py
    ~/blender-2.79b-linux-glibc219-x86_64/2.79/python get-pip.py
    cd blender-vraag
    ~/blender-2.79b-linux-glibc219-x86_64/2.79/ppip install -e .


This downloads a Python script which will download and install the current version of pip in your Blender's Python installation. 

The advantage of this approach is that you can now install Python packages at will. The catch is that this will only work with pure-Python libraries and Wheels compiled for Python 3.5.3 and your system.

To compile binary extensions, you will need python3.5m-devel, which has been dropped from the current official Ubuntu repositories.
