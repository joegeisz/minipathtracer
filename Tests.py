from SpecialObjects import *
from Scene import *
from Primatives import *
from utils import *
import matplotlib.pyplot as plt

def test1():
    # does the ray intersect the sphere correctly?
    intersect = Sphere([10,0,0],1).ray_intersect(Ray([0,0,0],[1,0,0]))
    if (intersect == np.array([9,0,0], dtype=float)).all():
        print("Test 1 correct")
    else:
        print("Test 1 failed: intersect is ", intersect, ", should be (9,0,0)")

def test2():
    #is the normal of the sphere calculated correctly?
    i,t,n = Sphere([0,0,10],2).ray_intersect_time_normal(Ray([0,0,0],[0,0,1]))
    if (n == np.array([0,0,-1], dtype=float)).all():
        print("Test 2 correct")
    else:
        print("Test 2 failed: normal is ", n, ", should be (0,0,-1)")


def test3():
    #bounces correctly?
    s1 = Sphere([10,0,0],1)
    s2 = Sphere([-10,0,0],1)
    ob,t,i,n =  Scene([s1,s2],Camera([0,0,0],[1,0,0],0,0,0)).object_hit(Ray([0,0,0],[1,0,0]))
    if ob == 0:
        print("Test 3 correct")
    else:
        print("Test 3 failed:  wrong object hit" , ob)

def test4():
    # does the plane reflect correctly?
    plane = Plane([0,0,1],1)
    cam = Camera([0,0,5],[0,0,0],10,10,10)
    o, t, i, n = Scene([plane],cam).object_hit(Ray([0,0,5],[0,0,-1]))
    if o != 0:
        print("Test 4 failed: didn't hit plane")
    elif (n != np.array([0,0,1])).any():
        print("Test 4 Failed: wrong normal")
    else: 
        print("Test 4 correct")
        
test1()
test2()
test3()
test4()

#plotting tests
def plot_test1():
    points = np.array([hemisphere_sample(np.array([1,0,0])) for i in range(1000)])
    plt.scatter(points[:,0],points[:,1])
    plt.title("should look like right side of sphere")
    plt.show()

plot_test1()