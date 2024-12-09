from Scene import *
from SpecialObjects import *
from Primatives import *
import matplotlib.pyplot as plt 


if __name__ == '__main__':
    plane = Plane([0,0,1],0, reflectance = [.5,.5,.5],emmitance = [0.1,0.1,0.1])
    Red_Sphere = Sphere([12,12,2],2, reflectance = [1,0,0], emmitance = [0,0,0])
    Blue_Sphere = Sphere([7,10,1],1, reflectance = [0,0,1], emmitance = [0,0,0])
    Green_Sphere = Sphere([11,8,0.5],0.5,reflectance = [0,1,0], emmitance = [0,0,0])
    Light_Sphere = Sphere([9,9,0.75],0.75, reflectance = [1,1,1], emmitance = [3,3,3])
    cam = Camera([0,0,5],[10,10,2],256,256,0.5)
    layout = Scene([Light_Sphere,Red_Sphere,Green_Sphere,Blue_Sphere,plane],cam)

    layout.save_path_trace_images(1000,n_processors=7)



