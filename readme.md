Vraag
=====
A high level API for Blender, modeled after JQuery
--------------------------------------------------
Vraag is Dutch for query, and this library allows you to query Blender data objects in a more concise and consistent way.

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
