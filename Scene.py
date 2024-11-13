from Classes import *
import matplotlib.pyplot as plt 

plane = Plane([0,0,1],0)
s1 = Sphere([0,100,10],50)
s2 = Sphere([50,40,10],20)
cam = Camera([0,0,10],[0,100,0],300,150,5)
layout = Scene([plane,s1,s2],cam)
img = layout.intersection_image()
#print(img)
plt.imshow(img)
plt.show()


