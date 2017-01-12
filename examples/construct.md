
Vraag.construct is a system to algorithmically compose objects and scene. It is inspired by OpenScad, but has a much better integration with Blender.

You can use the full power of Python for scripting construction, and the end result is a Blender scene which is fully editable. The subcomponents are just objects, with the assigned names and transformations, just as if they had been created by a user. They can then be animated using the usual means.



Basics
--------

The V().construct() method creates a root object, from which the construction starts.

```python
	root.cube()
```
This creates a simple cube in the center of the scene.

```python
	root.translate([3,0,0]).rotate(up, 45).cube()
```

This creates a simple cube in the center of the scene.
This creates a cube, which is first rotated around the z axis, then translated 3 units to the right. Transformations are applied in the reverse order they are invoked. The order does matter. It's easier to think of transformations like this: everyhing following this node will be translated by 3 units to the right.


```python
	root.cube().translate([0,0,1]).sphere()
```

This will create a sphere one unit above a cube, and parent the sphere to the cube. After construction, the sphere will follow any transformations of the cube.

This mechanism means it is very easy to create hierarchies of objects. Often, you will want to attach more than one object to the same parent:

```python
cube = root.cube()
cube.translate([0,0,1]).sphere()
cube.translate([0,0,-1]).sphere()
```

The cube node is saved to a variable, and the construction tree is extended two times. The transformation nodes don't result in Blender objects of their own, but they are used to set the local transformation matrix of object nodes further down the tree.

You can use Boolean operations to compose more complex objects, like in OpenScad:

```python
root.cube().difference(root.cylinder(r=0.5, height=1.1))
root.cube().union(root.translate([0.5,0.5,0]).cube())
```

See the examples for more ideas.
