from SpecialObjects import *
from Primatives import *

def test1():
    # does the ray intersect the sphere correctly?
    intersect = Sphere([10,0,0],1).ray_intersect(Ray([0,0,0],[1,0,0]))
    print(intersect)
    if (intersect == np.array([9,0,0], dtype=float)).all():
        print("Test 1 correct")
    else:
        print("Test 1 failed: intersect is ", intersect, ", should be (9,0,0)")


test1()