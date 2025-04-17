from Scene import *
from SpecialObjects import *
from Primatives import *
import matplotlib.pyplot as plt 
import cv2
import time

if __name__ == '__main__':
    plane = Plane([0,0,1], 0,
                   material_color = [1,0,0],
                   reflectance = [1,1,1],
                   emmitance = [0,0,0])

    plane2 = Plane([0,-0.1,1], 0,
                   material_color = [1,1,0],
                   reflectance = [1,0,1],
                   emmitance = [0,0,0])
    
    s1 = Sphere([10,10,2],2, 
                material_color=[1,0,0],
                reflectance = [1.0,0,0], 
                emmitance = [0,0,0])
    
    s2 = Sphere([7,10,1],1, 
                material_color = [1,0,0],
                reflectance = [0,0,1], 
                emmitance = [0,0,0])
    
    s3 = Sphere([10,7,0.5],0.5, 
                material_color = [1,0,0],
                reflectance = [0,1,0], 
                emmitance = [0,0,0])
    
    tri = Tri([12,5,5],[5,12,5],[12,12,5],
                material_color = [0,0,0],
                reflectance = [1,1,1], 
                emmitance = [2,2,2])
    
    tri2 = Tri([12,5,5],[5,5,5],[5,12,5],
                material_color = [0,0,0],
                reflectance = [1,1,1], 
                emmitance = [2,2,2])
    
    cam = Camera([0,0,5],[10,10,2],256,256,0.5)

    layout = Scene([s1,s2,s3,tri,tri2,plane],cam)

    plt.figure()
    plt.imshow(layout.object_image())

    renderedim = layout.path_trace_image(7*3,n_processors=7)
    np.save("image1.np",renderedim)
    

    # plt.figure()
    # plt.imshow(layout.normal_image())

    plt.show()


