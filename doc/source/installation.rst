Installation and using
========================


Shallow integration with Blender Python
-----------------------------------------
Unfortunately Blender does not have any default package management, which means it can be a pain to distribute slightly more complicated addons. Vraag therefore does not require external dependencies.

However, the vraag library is imported as a directory, thus the "vraag" folder must be in the PYTHONPATH. This can be accomplished by copying/linking it into blender's site-packages directory, or by adding the blender-vraag directory to the PYTHONPATH environment variable.

Currently, the Vraag library is solely developed under Linux, but it doesn't contain anything which should be impossible to run on Windows. Any suggestions, bug reports etc are welcome.

Vraag is now mostly working with Blender 2.8. There have been a lot of API changes in this major Blender update. At this point it is not clear how long 2.79 will stay around. This installation guide assumes 2.8.

One way to run examples or scripts is the following commandline:

..code-block:: bash
    PYTHONPATH=~/blender-vraag blender myfile.blend -P myscript.py

You have to make sure to invoke the right 'blender' binary. If you download a Blender release as an archive from the blender.org homepage, you can extract it anywhere on your harddrive. The binaries contained therein will work without further installation.

PIP
-----------------------------------------------

This has been tested on Linux (Ubuntu). It may not work for windows

.. code-block:: bash
    wget https://bootstrap.pypa.io/get-pip.py
    ~/blender-2.80-59f0db430a9-linux-glibc224-x86_64/2.80/python/bin/python3.7m get-pip.py
    cd blender-vraag
    ~/blender-2.80-59f0db430a9-linux-glibc224-x86_64/2.80/python/bin/pip install -e .


This downloads a Python script which will download and install the current version of pip in your Blender's Python installation. 

The advantage of this approach is that you can now install Python packages at will. The catch is that this will only
work with pure-Python libraries and Wheels compiled for the exact same version and your system.

