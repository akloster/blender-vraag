import sys
import numpy as np
sys.path.append(".")
from vraag import V

test_queries = ["object",
                "objects",
                "object#Cube",
                "#Cube",
                "@scene object",
                "@scene camera",
                "#Scene1 object#Suzanne"
                "camera",
                "lamp"
                ]

def test_query():
    for q in test_queries:
        print("V(\"%s\")" % q)
        print(V(q))

def test_array():
    print (V("objects").array.location)
    print (V("objects").array.scale)
    print (V("objects").array.rotation_euler)

def test_array2():
    a =  V("objects").array.location
    print (a)
    V("objects").array.location = a+1
    print(V("objects").array.location)
    try:
        V("objects").array.location = np.array([[0,1,2,3,4],[2,4,6,8]])
    except ValueError:
        pass

def test_verbs():
    print(list(V("object").map(lambda o: o.location)))
test_query()
test_array2()
#test_verbs()
