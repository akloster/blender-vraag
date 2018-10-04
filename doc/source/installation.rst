Installation and using
========================

Unfortunately Blender does not have any package management, which means it can be a pain to distribute slightly more complicated addons. Vraag therefore does not contain any third-party libraries (yet).

However, the vraag library is imported as a directory, thus the "vraag" folder must be in the PYTHONPATH. This can be accomplished by copying/linking it into blender's site-packages directory, or by adding the blender-vraag directory to the PYTHONPATH environment variable.


Currently, the Vraag library is solely developed under Linux, but it doesn't contain anything which should be impossible to run on Windows. Any suggestions, bug reports etc are welcome.

So far, Vraag does not support Blender 2.8. A lot has changed in the way to handle objects and scenes, so parts of the library may need a rethink.

One way to run examples or scripts is the following commandline:


PYTHONPATH=~/blender-vraag blender myfile.blend -P myscript.py



